#!/usr/bin/env python3
"""
Send a Telegram notification (and optionally the generated videos) using the
bot credentials in C:\\g\\ws\\.env  (TELEGRAM_BOT_TOKEN + a chat id).

Usage:
  python notify_telegram.py "message text"                 # text only
  python notify_telegram.py "caption" videos/x.mp4 ...      # send videos too
"""
import os
import sys
import mimetypes
from pathlib import Path
from urllib import request as _rq

ENV_PATH = Path(r"C:\g\ws\.env")


def load_env(path):
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip("'").strip('"')
    return env


def _multipart(fields, files):
    boundary = "----ccvboundary7MA4YWxkTrZu0gW"
    body = b""
    for k, v in fields.items():
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n").encode()
    for name, fp in files:
        fp = Path(fp)
        ctype = mimetypes.guess_type(fp.name)[0] or "application/octet-stream"
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; filename=\"{fp.name}\"\r\n"
                 f"Content-Type: {ctype}\r\n\r\n").encode()
        body += fp.read_bytes() + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return boundary, body


def api(token, method, fields, files=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    if files:
        boundary, body = _multipart(fields, files)
        headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
        req = _rq.Request(url, data=body, headers=headers)
    else:
        from urllib.parse import urlencode
        req = _rq.Request(url, data=urlencode(fields).encode())
    with _rq.urlopen(req, timeout=120) as r:
        return r.read().decode()


def main():
    env = load_env(ENV_PATH)
    token = env.get("TELEGRAM_BOT_TOKEN")
    chat = (env.get("TELEGRAM_OPS_CHAT_ID") or env.get("TELEGRAM_ANNOUNCE_CHAT_ID")
            or env.get("TELEGRAM_DRAFTS_CHAT_ID"))
    if not token or not chat:
        print("ERROR: missing TELEGRAM_BOT_TOKEN or chat id in .env", file=sys.stderr)
        sys.exit(1)
    msg = sys.argv[1] if len(sys.argv) > 1 else "done"
    vids = sys.argv[2:]
    print(api(token, "sendMessage", {"chat_id": chat, "text": msg, "parse_mode": "HTML",
                                     "disable_web_page_preview": "true"}))
    for v in vids:
        print(f"uploading {v} ...")
        print(api(token, "sendVideo",
                  {"chat_id": chat, "caption": Path(v).name}, files=[("video", v)]))


if __name__ == "__main__":
    main()
