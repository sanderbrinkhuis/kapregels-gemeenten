"""HTTP-ophaallaag met lokale opslag en herkomstregistratie.

Elke opgehaalde URL wordt ongewijzigd op schijf bewaard en vastgelegd in
data/manifest.jsonl (url, pad, tijdstip, HTTP-status, sha256, grootte,
content-type). Bestaat het bestand al, dan wordt het niet opnieuw opgehaald
(tenzij refresh=True), zodat een onderbroken run kan worden hervat.
"""

from __future__ import annotations

import hashlib
import json
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

_PKG_ROOT = Path(__file__).resolve().parent.parent
# Vanuit de broncode (ook bij `pip install -e .`): de projectmap. Anders: de map waarin je het commando draait.
ROOT = _PKG_ROOT if (_PKG_ROOT / "pyproject.toml").exists() else Path.cwd()
DATA = ROOT / "data"
MANIFEST = DATA / "manifest.jsonl"

USER_AGENT = "bomen-kapbeleid-onderzoek/0.1 (python-urllib)"
MIN_INTERVAL = 0.3  # seconden tussen requests per host
RETRIES = 4
TIMEOUT = 90

_manifest_lock = threading.Lock()
_host_locks: dict[str, threading.Lock] = {}
_host_last: dict[str, float] = {}
_host_guard = threading.Lock()


class FetchError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def build_url(base: str, params: dict | None = None) -> str:
    if not params:
        return base
    return base + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


def _throttle(host: str) -> None:
    with _host_guard:
        lock = _host_locks.setdefault(host, threading.Lock())
    with lock:
        wait = _host_last.get(host, 0) + MIN_INTERVAL - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _host_last[host] = time.monotonic()


def _record(entry: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    with _manifest_lock, MANIFEST.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def fetch(url: str, dest: Path, *, refresh: bool = False, context: str = "") -> bytes:
    """Haal url op naar dest (of lees dest als die al bestaat)."""
    if dest.exists() and not refresh:
        return dest.read_bytes()

    host = urllib.parse.urlsplit(url).netloc
    last_err: Exception | None = None
    for attempt in range(RETRIES):
        _throttle(host)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                body = resp.read()
                status = resp.status
                ctype = resp.headers.get("Content-Type", "")
            break
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2 ** attempt * 2)
                continue
            _record({"url": url, "path": None, "retrieved_at": now_iso(),
                     "status": e.code, "error": str(e), "context": context})
            raise FetchError(f"{url}: HTTP {e.code}") from e
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_err = e
            time.sleep(2 ** attempt * 2)
    else:
        _record({"url": url, "path": None, "retrieved_at": now_iso(),
                 "status": None, "error": str(last_err), "context": context})
        raise FetchError(f"{url}: {last_err}")

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    tmp.write_bytes(body)
    tmp.replace(dest)
    _record({
        "url": url,
        "path": str(dest.relative_to(ROOT)),
        "retrieved_at": now_iso(),
        "status": status,
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        "content_type": ctype,
        "context": context,
    })
    return body
