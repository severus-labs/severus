# severus/utils/crypto.py
import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def derive_key_from_totp_secret(totp_secret: str, salt: bytes = b'severus_salt') -> bytes:
    """Derive encryption key from TOTP secret"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(totp_secret.encode()))
    return key

def encrypt_data(data: dict, totp_secret: str) -> bytes:
    """Encrypt data dictionary to bytes"""
    key = derive_key_from_totp_secret(totp_secret)
    f = Fernet(key)
    
    json_data = json.dumps(data).encode()
    encrypted_data = f.encrypt(json_data)
    return encrypted_data

def decrypt_data(encrypted_data: bytes, totp_secret: str) -> dict:
    """Decrypt bytes back to data dictionary"""
    key = derive_key_from_totp_secret(totp_secret)
    f = Fernet(key)
    
    decrypted_bytes = f.decrypt(encrypted_data)
    data = json.loads(decrypted_bytes.decode())
    return data

def save_encrypted_file(data: dict, file_path: str, totp_secret: str):
    """Encrypt and save data to file"""
    encrypted_data = encrypt_data(data, totp_secret)
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

def load_encrypted_file(file_path: str, totp_secret: str) -> dict:
    """Load and decrypt data from file"""
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    return decrypt_data(encrypted_data, totp_secret)

# Save secret
# secret_data = {"name": "stripe-key", "password": "sk_live_123", "url": "stripe.com"}
# save_encrypted_file(secret_data, "blobs/stripe-key.enc", totp_secret)

# Read secret  
# secret_data = load_encrypted_file("blobs/stripe-key.enc", totp_secret)