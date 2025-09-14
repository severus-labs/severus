import requests
import json
import secrets
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Placeholder server URL - replace with your actual server
# SHARE_SERVER_URL = "https://api.severus.dev"
SHARE_SERVER_URL = "http://localhost:8080"

def generate_share_code(length=12):
    """Generate a random share code like 7X9K-M4P2-B8Q1"""
    chars = string.ascii_uppercase + string.digits
    code = ''.join(secrets.choice(chars) for _ in range(length))
    # Format as XXXX-XXXX-XXXX
    return f"{code[:4]}-{code[4:8]}-{code[8:12]}"

def derive_key_from_code(share_code: str) -> bytes:
    """Derive encryption key from share code"""
    # Remove hyphens and use as password
    password = share_code.replace('-', '').encode()
    salt = b'severus_share_salt_v1'  # Fixed salt for share codes
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt_for_sharing(data: dict, share_code: str) -> bytes:
    """Encrypt data for sharing using share code"""
    key = derive_key_from_code(share_code)
    f = Fernet(key)
    
    json_data = json.dumps(data).encode()
    encrypted_data = f.encrypt(json_data)
    return encrypted_data

def decrypt_from_sharing(encrypted_data: bytes, share_code: str) -> dict:
    """Decrypt shared data using share code"""
    key = derive_key_from_code(share_code)
    f = Fernet(key)
    
    decrypted_bytes = f.decrypt(encrypted_data)
    data = json.loads(decrypted_bytes.decode())
    return data

def check_code_availability(share_code: str) -> bool:
    """Check if share code is available (not in use)"""
    try:
        response = requests.get(f"{SHARE_SERVER_URL}/check/{share_code}", timeout=10)
        return response.status_code == 404  # 404 means code is available
    except requests.RequestException:
        return False

def upload_shared_data(share_code: str, encrypted_data: bytes) -> bool:
    """Upload encrypted data to server"""
    try:
        payload = {
            "code": share_code,
            "data": base64.b64encode(encrypted_data).decode(),
            "expires_minutes": 10
        }
        response = requests.post(f"{SHARE_SERVER_URL}/share", json=payload, timeout=30)
        return response.status_code == 201
    except requests.RequestException:
        return False

def download_shared_data(share_code: str) -> bytes:
    """Download and decrypt shared data"""
    try:
        response = requests.get(f"{SHARE_SERVER_URL}/receive/{share_code}", timeout=30)
        if response.status_code == 200:
            data = response.json()
            return base64.b64decode(data["data"])
        elif response.status_code == 404:
            raise Exception("Share code not found or expired")
        elif response.status_code == 410:
            raise Exception("Share code already used")
        else:
            raise Exception(f"Server error: {response.status_code}")
    except requests.RequestException as e:
        raise Exception(f"Network error: {e}")