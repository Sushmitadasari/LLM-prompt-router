import json
from pathlib import Path

# log file path
LOG_FILE = Path("route_log.jsonl")


def log_route(intent, confidence, user_message, final_response):
    """
    Logs routing decisions into route_log.jsonl
    """

    entry = {
        "intent": intent,
        "confidence": confidence,
        "user_message": user_message,
        "final_response": final_response
    }

    with open(LOG_FILE, "a") as file:
        file.write(json.dumps(entry) + "\n")