import pyotp
import qrcode

def generate_totp_secret():
    """Generate a new TOTP secret"""
    return pyotp.random_base32()

def generate_qr_code(secret, user_email="user@example.com", issuer="Severus"):
    """Generate QR code for TOTP setup"""
    # Create the provisioning URI
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user_email,
        issuer_name=issuer
    )
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=1, border=1)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    
    # Print to terminal
    qr.print_ascii()
    
    return totp_uri

def verify_totp(secret, token):
    """Verify a TOTP token"""
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)