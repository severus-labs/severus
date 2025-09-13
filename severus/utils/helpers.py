# severus/utils/helpers.py
import re

def slugify(text):
    """Convert text to a safe filename slug"""
    # Convert to lowercase and replace spaces with hyphens
    text = text.lower().strip()
    # Remove special characters, keep only alphanumeric and hyphens
    text = re.sub(r'[^a-z0-9\-]', '-', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text