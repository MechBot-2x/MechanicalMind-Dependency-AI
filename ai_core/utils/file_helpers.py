# ai_core/utils/file_helpers.py
def safe_read_file(path):
    """Read file content safely"""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception:
        return None
