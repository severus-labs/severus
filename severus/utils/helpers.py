import click
import re
from severus.utils import helpers
from datetime import datetime

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
    
def time_ago(timestamp_str):
    """Convert timestamp to human-readable time ago"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            minutes = diff.seconds // 60
            return f"{minutes} min ago"
    except:
        return "unknown"
    
def validate_email(ctx, param, value):
    """Validate email format using regex"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, value):
        raise click.BadParameter('Please enter a valid email address')
    return value