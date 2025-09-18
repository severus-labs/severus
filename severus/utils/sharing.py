import requests
import json
import secrets
import string
from cryptography.fernet import Fernet
import base64
import urllib3

# Disable SSL warnings (optional)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SHARE_SERVER_URL = "https://54.242.124.127:8080"

def generate_share_id(length=12):
    """Generate a random share ID like 7X9K-M4P2-B8Q1"""
    chars = string.ascii_uppercase + string.digits
    code = ''.join(secrets.choice(chars) for _ in range(length))
    return f"{code[:4]}-{code[4:8]}-{code[8:12]}"

def generate_private_key() -> bytes:
    """Generate a random private key for encryption"""
    return Fernet.generate_key()

def encrypt_for_sharing(data: dict, private_key: bytes) -> bytes:
    """Encrypt data using private key"""
    f = Fernet(private_key)
    json_data = json.dumps(data).encode()
    encrypted_data = f.encrypt(json_data)
    return encrypted_data

def decrypt_from_sharing(encrypted_data: bytes, private_key: bytes) -> dict:
    """Decrypt shared data using private key"""
    f = Fernet(private_key)
    decrypted_bytes = f.decrypt(encrypted_data)
    data = json.loads(decrypted_bytes.decode())
    return data

def check_code_availability(share_id: str) -> bool:
    """Check if share ID is available (not in use)"""
    try:
        response = requests.get(f"{SHARE_SERVER_URL}/check/{share_id}", timeout=10, verify=False)
        return response.status_code == 404  # 404 means ID is available
    except requests.RequestException:
        return False

def upload_shared_data(share_id: str, encrypted_data: bytes) -> bool:
    """Upload encrypted data to server using ID"""
    try:
        payload = {
            "code": share_id,  # Server uses this as lookup ID
            "data": base64.b64encode(encrypted_data).decode(),
            "expires_minutes": 10
        }
        response = requests.post(f"{SHARE_SERVER_URL}/share", json=payload, timeout=30, verify=False)
        return response.status_code == 201
    except requests.RequestException:
        return False

def download_shared_data(share_id: str) -> bytes:
    """Download encrypted data using ID"""
    try:
        response = requests.get(f"{SHARE_SERVER_URL}/receive/{share_id}", timeout=30, verify=False)
        if response.status_code == 200:
            data = response.json()
            return base64.b64decode(data["data"])
        elif response.status_code == 404:
            raise Exception("Share ID not found or expired")
        elif response.status_code == 410:
            raise Exception("Share ID already used")
        else:
            raise Exception(f"Server error: {response.status_code}")
    except requests.RequestException as e:
        raise Exception(f"Network error: {e}")