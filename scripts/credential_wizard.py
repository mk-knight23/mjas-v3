#!/usr/bin/env python3
"""
MJAS v3.0 - Secure Credential Wizard
Encrypts credentials immediately using Fernet (AES-128)
"""

import getpass
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mjas.core.vault import CredentialVault


def main():
    print("\n" + "=" * 60)
    print("  MJAS v3.0 - Secure Credential Setup")
    print("=" * 60)
    print()
    print("Your credentials will be encrypted with AES-128 (Fernet).")
    print("They are NEVER stored in plain text.")
    print()

    credentials = {}

    # Candidate Profile (from user)
    print("--- Candidate Profile (Pre-filled) ---")
    credentials["CANDIDATE_NAME"] = "Musharraf Kazi"
    credentials["CANDIDATE_EMAIL"] = "kazimusharraf1234@gmail.com"
    credentials["CANDIDATE_PHONE"] = "+919765490536"
    credentials["CANDIDATE_GITHUB"] = "https://github.com/mk-knight23"
    credentials["CANDIDATE_LINKEDIN"] = "https://www.linkedin.com/in/kazi-musharraf-0674871a4"
    print(f"Name: {credentials['CANDIDATE_NAME']}")
    print(f"Email: {credentials['CANDIDATE_EMAIL']}")
    print(f"Phone: {credentials['CANDIDATE_PHONE']}")
    print()

    # LinkedIn
    print("--- LinkedIn Credentials ---")
    credentials["LINKEDIN_EMAIL"] = input(f"LinkedIn email [{credentials['CANDIDATE_EMAIL']}]: ").strip() or credentials["CANDIDATE_EMAIL"]
    credentials["LINKEDIN_PASSWORD"] = getpass.getpass("LinkedIn password: ")
    if not credentials["LINKEDIN_PASSWORD"]:
        print("WARNING: No password provided for LinkedIn")
    print()

    # Indeed
    print("--- Indeed Credentials ---")
    credentials["INDEED_EMAIL"] = input(f"Indeed email [{credentials['CANDIDATE_EMAIL']}]: ").strip() or credentials["CANDIDATE_EMAIL"]
    credentials["INDEED_PASSWORD"] = getpass.getpass("Indeed password: ")
    print()

    # Wellfound / AngelList
    print("--- Wellfound (AngelList) Credentials ---")
    credentials["WELLFOUND_EMAIL"] = input(f"Wellfound email [{credentials['CANDIDATE_EMAIL']}]: ").strip() or credentials["CANDIDATE_EMAIL"]
    credentials["WELLFOUND_PASSWORD"] = getpass.getpass("Wellfound password: ")
    print()

    # Naukri (India)
    print("--- Naukri.com Credentials ---")
    credentials["NAUKRI_EMAIL"] = input(f"Naukri email [{credentials['CANDIDATE_EMAIL']}]: ").strip() or credentials["CANDIDATE_EMAIL"]
    credentials["NAUKRI_PASSWORD"] = getpass.getpass("Naukri password: ")
    print()

    # Gmail (for verification codes)
    print("--- Gmail App Password ---")
    print("Note: This is NOT your regular Gmail password.")
    print("Create one at: Google Account > Security > 2-Step Verification > App passwords")
    credentials["GMAIL_EMAIL"] = input(f"Gmail [{credentials['CANDIDATE_EMAIL']}]: ").strip() or credentials["CANDIDATE_EMAIL"]
    credentials["GMAIL_PASSWORD"] = getpass.getpass("Gmail app-specific password: ")
    print()

    # Confirm and encrypt
    print("=" * 60)
    confirm = input("Encrypt and save these credentials? [Y/n]: ").strip().lower()
    if confirm not in ("", "y", "yes"):
        print("Aborted. No credentials saved.")
        return 1

    # Create vault and encrypt
    try:
        vault = CredentialVault()
        vault.encrypt_credentials(credentials)

        print()
        print("✅ Credentials encrypted successfully!")
        print(f"   Key file: {vault.key_file}")
        print(f"   Encrypted data: {vault.creds_file}")
        print()
        print("IMPORTANT:")
        print("- Keep the .key file safe - without it, credentials cannot be recovered")
        print("- Never commit the .key file or .encrypted file to git")
        print("- Back up the .key file securely (password manager, etc.)")
        print()
        print("Next step: Run 'python -m mjas stats' to verify setup")

        return 0

    except Exception as e:
        print(f"\n❌ Error encrypting credentials: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
