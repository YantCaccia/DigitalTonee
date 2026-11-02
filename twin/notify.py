import json
import os
from datetime import datetime, timezone
from pathlib import Path

import httpx

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"


def _log(kind: str, payload: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    entry = {"ts": datetime.now(timezone.utc).isoformat(), **payload}
    with (LOG_DIR / f"{kind}.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _telegram(text: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not (token and chat_id):
        return
    try:
        httpx.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10,
        )
    except httpx.HTTPError:
        pass  # la notifica non deve mai rompere la chat


def notify(kind: str, payload: dict, text: str) -> None:
    _log(kind, payload)
    _telegram(text)
