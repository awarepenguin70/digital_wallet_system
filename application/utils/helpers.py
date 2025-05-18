import json
import os
from datetime import datetime
from ..config import Config

class Logger:
    @staticmethod
    def log_event(user, action, details=""):
        if not os.path.exists(Config.LOG_FILE):
            logs = []
        else:
            with open(Config.LOG_FILE, 'r') as f:
                logs = json.load(f) if os.path.getsize(Config.LOG_FILE) > 0 else []

        logs.append({
            "user": user,
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

        with open(Config.LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=4)