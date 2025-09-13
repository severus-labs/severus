import json
from datetime import datetime

def save_config(config_path, email, totp_secret):
    config_data = {
        "email": email,
        "secret": totp_secret,
        "created_at": datetime.now().isoformat(),
    }
    
    with open(config_path, "w") as file:
        json.dump(config_data, file, indent=2)
    
    return config_path

def load_config(config_path):
    if not config_path.exists():
        return None
    
    with open(config_path, "r") as file:
        return json.load(file)
