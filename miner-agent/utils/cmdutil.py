import json

def ret(success: bool, message: str):
    print(json.dumps({"success": success, "message": message}))