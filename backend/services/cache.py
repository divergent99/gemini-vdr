import json
import hashlib
import time
from backend.config import CACHE_DIR
from backend.logger import log


def doc_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _get_collection():
    """Return ChromaDB collection, creating it if needed. Returns None on failure."""
    try:
        import chromadb
        client = chromadb.PersistentClient(path=CACHE_DIR)
        return client.get_or_create_collection(
            name="analysis_cache",
            metadata={"description": "VDR Voice Intelligence — Gemini analysis cache"},
        )
    except Exception as e:
        log(f"ChromaDB unavailable — caching disabled: {e}", "WARN")
        return None


def cache_get(key: str) -> dict | None:
    """Return cached analysis dict for this doc hash, or None on miss."""
    col = _get_collection()
    if not col:
        return None
    try:
        result = col.get(ids=[key], include=["documents"])
        if result and result["ids"]:
            log(f"Cache HIT for {key[:12]}...", "OK")
            return json.loads(result["documents"][0])
    except Exception as e:
        log(f"Cache get error: {e}", "WARN")
    return None


def cache_put(key: str, analysis: dict, folder_path: str = "") -> None:
    """Store analysis result in ChromaDB cache."""
    col = _get_collection()
    if not col:
        return
    try:
        col.upsert(
            ids=[key],
            documents=[json.dumps(analysis)],
            metadatas=[{
                "folder":     folder_path,
                "cached_at":  time.strftime("%Y-%m-%dT%H:%M:%S"),
            }],
        )
        log(f"Cache stored for {key[:12]}...", "OK")
    except Exception as e:
        log(f"Cache put error: {e}", "WARN")
