import json
import os

def read_json(path):
    """Safely read JSON file — auto-create [] if missing or invalid"""
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write('[]')
        return []

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        # If file corrupted or invalid, reset to empty array
        with open(path, 'w', encoding='utf-8') as f:
            f.write('[]')
        return []

def write_json(path, data):
    """Safely write JSON file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
