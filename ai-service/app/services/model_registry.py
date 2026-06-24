import joblib
import json
from datetime import datetime
from pathlib import Path
from app.core.config import settings

class ModelRegistry:
    def __init__(self):
        self.registry_path = Path(settings.MODEL_PATH) / "registry.json"
        self._ensure()

    def _ensure(self):
        if not self.registry_path.exists():
            self._save({"models": [], "active": None})

    def _load(self):
        return json.loads(self.registry_path.read_text())

    def _save(self, data):
        self.registry_path.write_text(json.dumps(data, indent=2))

    def register(self, version: str, metrics: dict, path: str):
        data = self._load()
        entry = {"version": version, "metrics": metrics, "path": path, "created_at": datetime.utcnow().isoformat()}
        data["models"].append(entry)
        data["active"] = version
        self._save(data)

    def get_active(self):
        data = self._load()
        if not data.get("active"):
            return None
        for m in data["models"]:
            if m["version"] == data["active"]:
                return m
        return None

registry = ModelRegistry()
