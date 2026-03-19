#!/usr/bin/env python3
"""
Secure Credential Setup for ElevenLabs API

This module provides secure methods for storing and validating
ElevenLabs API credentials. It uses getpass for masked input
and stores credentials in a .env file with restricted permissions.

Security Features:
    - Masked password-style input (characters not displayed)
    - .env file created with 0600 permissions (owner read/write only)
    - API key validation before storage
    - No credentials logged or printed

Usage:
    Run directly: python -m elevenlabs_connect.secure_setup
    Or import:    from secure_setup import setup_credentials

Author: Chad Hendren
Created: March 2026
"""

import os
import sys
import stat
import getpass
import logging
from pathlib import Path
from typing import Optional, Tuple

import requests
from dotenv import load_dotenv

# Configure logging - note: we never log API keys!
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ElevenLabs API configuration
API_BASE_URL = "https://api.elevenlabs.io/v1"

# Default .env location
DEFAULT_ENV_PATH = Path.cwd() / ".env"


def mask_api_key(api_key: str) -> str:
    """
    Mask an API key for safe display in logs/output.
    
    Shows first 4 and last 4 characters only.
    Example: "sk_abcd1234...xyz9" -> "sk_a...xyz9"
    
    Args:
        api_key: The full API key
        
    Returns:
        str: Masked version safe for display
    """
    if len(api_key) < 12:
        return "****"
    return f"{api_key[:4]}...{api_key[-4:]}"


def validate_api_key(api_key: str) -> Tuple[bool, str]:
    """
    Validate an ElevenLabs API key by checking the user's subscription.
    
    This makes a lightweight API call to verify the key is valid
    and returns information about the account.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
            - is_valid: True if key is valid
            - message: Account tier info or error message
            
    Example:
        >>> is_valid, msg = validate_api_key("sk_abc123...")
        >>> if is_valid:
        ...     print(f"Valid key! Account: {msg}")
    """
    logger.info("Validating API key...")
    
    try:
        # Use the subscription endpoint for validation
        # This is lightweight and returns account info
        response = requests.get(
            f"{API_BASE_URL}/user/subscription",
            headers={"xi-api-key": api_key},
            timeout=10
        )
        
        if response.status_code == 200:
            # Key is valid - extract account info
            data = response.json()
            tier = data.get("tier", "unknown")
            character_limit = data.get("character_limit", 0)
            characters_used = data.get("character_count", 0)
            
            msg = (
                f"Account: {tier} tier | "
                f"Characters: {characters_used:,}/{character_limit:,}"
            )
            logger.info(f"API key valid: {tier} tier")
            return True, msg
            
        elif response.status_code == 401:
            logger.warning("Invalid API key (401 Unauthorized)")
            return False, "Invalid API key - authentication failed"
            
        elif response.status_code == 403:
            logger.warning("API key lacks permissions (403 Forbidden)")
            return False, "API key valid but lacks required permissions"
            
        else:
            logger.warning(f"Unexpected response: {response.status_code}")
            return False, f"Unexpected response: {response.status_code}"
            
    except requests.exceptions.Timeout:
        logger.error("Connection timed out")
        return False, "Connection timed out - please try again"
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Connection error: {e}")
        return False, f"Connection error: {str(e)}"


def prompt_for_api_key() -> str:
    """
    Securely prompt the user for their ElevenLabs API key.
    
    Uses getpass for masked input - characters are not displayed.
    
    Returns:
        str: The entered API key
    """
    print("\n" + "=" * 60)
    print("ElevenLabs API Key Setup")
    print("=" * 60)
    print("\nYour API key will be:")
    print("  - Hidden while typing (password-style input)")
    print("  - Stored locally in .env with restricted permissions")
    print("  - Never logged or transmitted insecurely")
    print("\nGet your API key: https://elevenlabs.io/app/settings/api-keys")
    print("-" * 60)
    
    # getpass hides input - user won't see characters as they type
    api_key = getpass.getpass("\nEnter your ElevenLabs API key: ")
    
    # Strip whitespace that might be accidentally included
    return api_key.strip()


def save_to_env(
    api_key: str,
    env_path: Optional[Path] = None
) -> Path:
    """
    Save the API key to a .env file with secure permissions.
    
    Creates or updates the .env file and sets file permissions
    to 0600 (owner read/write only) on Unix systems.
    
    Args:
        api_key: The API key to save
        env_path: Optional custom path for .env file
        
    Returns:
        Path: Path to the created/updated .env file
    """
    env_path = env_path or DEFAULT_ENV_PATH
    
    # Read existing .env content if it exists
    existing_content = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    existing_content[key.strip()] = value.strip()
    
    # Update with new API key
    existing_content['ELEVENLABS_API_KEY'] = api_key
    
    # Write back all content
    with open(env_path, 'w') as f:
        f.write("# ElevenLabs API Configuration\n")
        f.write("# This file contains sensitive credentials - DO NOT COMMIT\n")
        f.write("# File should have 0600 permissions (owner read/write only)\n\n")
        
        for key, value in existing_content.items():
            f.write(f"{key}={value}\n")
    
    # Set restrictive permissions (Unix only)
    # 0600 = owner can read/write, no access for group or others
    try:
        os.chmod(env_path, stat.S_IRUSR | stat.S_IWUSR)  # 0600
        logger.info(f"Set file permissions to 0600 on {env_path}")
    except Exception as e:
        # Non-fatal on Windows or if permissions can't be set
        logger.warning(f"Could not set file permissions: {e}")
    
    return env_path


def ensure_gitignore(directory: Optional[Path] = None) -> None:
    """
    Ensure .env is in .gitignore to prevent accidental commits.
    
    Creates or updates .gitignore to include .env pattern.
    
    Args:
        directory: Directory containing .gitignore (default: cwd)
    """
    directory = directory or Path.cwd()
    gitignore_path = directory / ".gitignore"
    
    patterns_to_add = [".env", ".env.*", "*.env"]
    
    existing_patterns = set()
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            existing_patterns = {line.strip() for line in f if line.strip()}
    
    # Add missing patterns
    patterns_needed = [p for p in patterns_to_add if p not in existing_patterns]
    
    if patterns_needed:
        with open(gitignore_path, 'a') as f:
            if existing_patterns:  # Add newline if file had content
                f.write("\n")
            f.write("# Sensitive environment files\n")
            for pattern in patterns_needed:
                f.write(f"{pattern}\n")
        
        logger.info(f"Updated .gitignore with patterns: {patterns_needed}")


def setup_credentials(
    env_path: Optional[Path] = None,
    interactive: bool = True
) -> bool:
    """
    Complete credential setup workflow.
    
    This function:
    1. Prompts for API key (if interactive)
    2. Validates the key with ElevenLabs API
    3. Saves to .env with secure permissions
    4. Ensures .env is in .gitignore
    
    Args:
        env_path: Optional custom path for .env file
        interactive: If True, prompt for input; if False, validate env only
        
    Returns:
        bool: True if setup was successful
    """
    env_path = env_path or DEFAULT_ENV_PATH
    
    if interactive:
        # Get API key from user with masked input
        api_key = prompt_for_api_key()
        
        if not api_key:
            print("\nNo API key entered. Setup cancelled.")
            return False
        
        # Validate the key
        print(f"\nValidating key: {mask_api_key(api_key)}")
        is_valid, message = validate_api_key(api_key)
        
        if not is_valid:
            print(f"\n❌ Validation failed: {message}")
            print("Please check your API key and try again.")
            return False
        
        print(f"\n✅ API key validated!")
        print(f"   {message}")
        
        # Save to .env
        saved_path = save_to_env(api_key, env_path)
        print(f"\n✅ Credentials saved to: {saved_path}")
        
        # Update .gitignore
        ensure_gitignore(env_path.parent)
        print("✅ .gitignore updated to exclude .env files")
        
        print("\n" + "=" * 60)
        print("Setup complete! You can now use the ElevenLabs API.")
        print("=" * 60 + "\n")
        
        return True
    
    else:
        # Non-interactive: just validate existing key
        load_dotenv(env_path)
        api_key = os.environ.get("ELEVENLABS_API_KEY")
        
        if not api_key:
            logger.warning("No API key found in environment")
            return False
        
        is_valid, _ = validate_api_key(api_key)
        return is_valid


def get_account_info(api_key: Optional[str] = None) -> dict:
    """
    Get full account information from ElevenLabs.
    
    Args:
        api_key: Optional API key (uses environment if not provided)
        
    Returns:
        dict: Account information including tier, usage, limits
    """
    load_dotenv()
    api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    
    if not api_key:
        raise ValueError("No API key provided or found in environment")
    
    response = requests.get(
        f"{API_BASE_URL}/user/subscription",
        headers={"xi-api-key": api_key},
        timeout=10
    )
    response.raise_for_status()
    
    return response.json()


if __name__ == "__main__":
    """
    Run credential setup when executed directly.
    
    Usage:
        python secure_setup.py          # Interactive setup
        python secure_setup.py --check  # Validate existing credentials
    """
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        # Validate mode
        print("Checking existing credentials...")
        is_valid = setup_credentials(interactive=False)
        sys.exit(0 if is_valid else 1)
    else:
        # Interactive setup
        success = setup_credentials(interactive=True)
        sys.exit(0 if success else 1)
