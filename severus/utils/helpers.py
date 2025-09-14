# severus/utils/helpers.py
import re
from severus.utils import helpers

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

def resolve_env_name(env_name, current_project):
    """Convert user input to actual vault name"""
    if env_name.startswith('.env'):
        if env_name == '.env':
            return f"{current_project}-env"
        else:
            # .env.local -> myapp-env-local
            suffix = env_name.replace('.env.', '')
            return f"{current_project}-env-{suffix}"
    
    elif env_name == 'env':
        return f"{current_project}-env"
    
    elif env_name.startswith('env-'):
        # env-local -> myapp-env-local
        suffix = env_name.replace('env-', '')
        return f"{current_project}-env-{suffix}"
    
    else:
        # Direct name like myapp-env or severus-env-local
        return helpers.slugify(env_name)