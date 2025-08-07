import json
import os
from typing import Dict, Any


BASE_DIR = os.path.join(".streamlit", "user_data")


def _ensure_base_dir() -> None:
    if not os.path.isdir(BASE_DIR):
        os.makedirs(BASE_DIR, exist_ok=True)


def _store_path(username: str) -> str:
    _ensure_base_dir()
    safe_username = username.replace("/", "_")
    return os.path.join(BASE_DIR, f"{safe_username}.json")


def _default_store() -> Dict[str, Any]:
    return {
        "market": {"chat_history": {}, "current_chat_id": None},
        "reader": {"chat_history": {}, "current_chat_id": None},
        "conviction": {"chat_history": {}, "current_chat_id": None},
    }


def load_user_store(username: str) -> Dict[str, Any]:
    path = _store_path(username)
    if not os.path.exists(path):
        return _default_store()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Ensure required keys exist
        defaults = _default_store()
        for key in defaults:
            data.setdefault(key, defaults[key])
        return data
    except Exception:
        return _default_store()


def save_user_store(username: str, store: Dict[str, Any]) -> None:
    path = _store_path(username)
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


