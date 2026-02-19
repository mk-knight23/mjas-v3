"""Encrypted credential vault using Fernet (AES-128)."""

import json
import os
from pathlib import Path
from typing import Dict, Optional

from cryptography.fernet import Fernet
from pydantic import BaseModel, ConfigDict, Field


class Credentials(BaseModel):
    """Platform credentials model."""

    model_config = ConfigDict(populate_by_name=True)

    # LinkedIn
    linkedin_email: Optional[str] = Field(None, alias="LINKEDIN_EMAIL")
    linkedin_password: Optional[str] = Field(None, alias="LINKEDIN_PASSWORD")

    # Indeed
    indeed_email: Optional[str] = Field(None, alias="INDEED_EMAIL")
    indeed_password: Optional[str] = Field(None, alias="INDEED_PASSWORD")

    # Wellfound
    wellfound_email: Optional[str] = Field(None, alias="WELLFOUND_EMAIL")
    wellfound_password: Optional[str] = Field(None, alias="WELLFOUND_PASSWORD")

    # Naukri
    naukri_email: Optional[str] = Field(None, alias="NAUKRI_EMAIL")
    naukri_password: Optional[str] = Field(None, alias="NAUKRI_PASSWORD")

    # Gmail (for verification codes)
    gmail_email: Optional[str] = Field(None, alias="GMAIL_EMAIL")
    gmail_password: Optional[str] = Field(None, alias="GMAIL_PASSWORD")


class CredentialVault:
    """Manages encrypted credential storage."""

    def __init__(
        self,
        key_file: Path = Path("config/credentials.key"),
        creds_file: Path = Path("config/credentials.env.encrypted")
    ):
        self.key_file = key_file
        self.creds_file = creds_file
        self._fernet: Optional[Fernet] = None

    def _ensure_key(self) -> Fernet:
        """Generate or load encryption key."""
        if self._fernet:
            return self._fernet

        if self.key_file.exists():
            key = self.key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            self.key_file.parent.mkdir(parents=True, exist_ok=True)
            self.key_file.write_bytes(key)
            os.chmod(self.key_file, 0o600)  # User read/write only

        self._fernet = Fernet(key)
        return self._fernet

    def encrypt_credentials(self, data: Dict[str, str]) -> None:
        """Encrypt and save credentials."""
        fernet = self._ensure_key()
        json_data = json.dumps(data).encode()
        encrypted = fernet.encrypt(json_data)
        self.creds_file.parent.mkdir(parents=True, exist_ok=True)
        self.creds_file.write_bytes(encrypted)
        os.chmod(self.creds_file, 0o600)

    def decrypt_credentials(self) -> Dict[str, str]:
        """Decrypt and return credentials."""
        if not self.creds_file.exists():
            return {}

        fernet = self._ensure_key()
        encrypted = self.creds_file.read_bytes()
        json_data = fernet.decrypt(encrypted)
        return json.loads(json_data.decode())

    def get_credentials(self) -> Credentials:
        """Get credentials as validated model."""
        data = self.decrypt_credentials()
        return Credentials(**data)

    def rotate_key(self) -> None:
        """Generate new key and re-encrypt credentials."""
        data = self.decrypt_credentials()
        self._fernet = None
        self.key_file.unlink(missing_ok=True)
        self.encrypt_credentials(data)
