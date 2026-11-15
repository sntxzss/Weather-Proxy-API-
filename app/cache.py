import time 
from typing import Any, Optional

class TTLCache:
    def __init__(self, ttl: float):
        self.ttl = ttl
        self._store: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        key = key.lower()
        entry = self._store.get(key)
        if entry is None:
            return None

        saved_at, data = entry
        if time.monotonic() - saved_at > self.ttl:
            del self._store[key]
            return None

        return data

    def set(self, key: str, data: Any) -> None:
        key = key.lower()
        self._store[key] = (time.monotonic(), data)
    

