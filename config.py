import json
import os

DEFAULT_CONFIG = {
    "confidence_thresholds": {
        "spam": 60,
        "bug": 50,
        "suggestion": 40,
        "abuse": 70,
        "default": 50,
    },
    "severity_escalation_sentiments": ["angry", "frustrated"],
    "max_agent_steps": 8,
}

CONFIG_PATH = os.getenv("GUARDIAN_CONFIG", "guardian_config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            user_config = json.load(f)
        merged = {**DEFAULT_CONFIG, **user_config}
        merged["confidence_thresholds"] = {
            **DEFAULT_CONFIG["confidence_thresholds"],
            **user_config.get("confidence_thresholds", {}),
        }
        return merged
    return DEFAULT_CONFIG.copy()

def get_threshold(intent):
    config = load_config()
    thresholds = config["confidence_thresholds"]
    return thresholds.get(intent, thresholds["default"])

def get_config():
    return load_config()
