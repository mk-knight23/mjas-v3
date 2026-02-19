"""Unit tests for the encrypted credential vault."""

import pytest
import os
from pathlib import Path
from mjas.core.vault import CredentialVault, Credentials


@pytest.fixture
def temp_vault(tmp_path):
    """Create a temporary vault for testing."""
    key_file = tmp_path / "test.key"
    creds_file = tmp_path / "test.env.enc"
    return CredentialVault(key_file=key_file, creds_file=creds_file)


def test_vault_generates_key_if_missing(temp_vault):
    """Test that vault generates a new key if one doesn't exist."""
    assert not temp_vault.key_file.exists()
    temp_vault._ensure_key()
    assert temp_vault.key_file.exists()


def test_vault_encrypts_and_decrypts(temp_vault):
    """Test encryption and decryption roundtrip."""
    data = {"LINKEDIN_EMAIL": "test@example.com", "LINKEDIN_PASSWORD": "secret123"}
    temp_vault.encrypt_credentials(data)

    decrypted = temp_vault.decrypt_credentials()
    assert decrypted["LINKEDIN_EMAIL"] == "test@example.com"
    assert decrypted["LINKEDIN_PASSWORD"] == "secret123"


def test_credentials_model_validation():
    """Test Pydantic credentials model validation."""
    creds = Credentials(
        linkedin_email="test@example.com",
        linkedin_password="secret123"
    )
    assert creds.linkedin_email == "test@example.com"
    assert creds.linkedin_password == "secret123"


def test_credentials_model_with_aliases():
    """Test credentials model with environment variable aliases."""
    data = {
        "LINKEDIN_EMAIL": "test@example.com",
        "LINKEDIN_PASSWORD": "secret123",
        "INDEED_EMAIL": "indeed@example.com",
        "INDEED_PASSWORD": "indeed_pass"
    }
    creds = Credentials(**data)
    assert creds.linkedin_email == "test@example.com"
    assert creds.indeed_email == "indeed@example.com"


def test_vault_file_permissions(temp_vault):
    """Test that key file has restricted permissions (0o600)."""
    temp_vault._ensure_key()
    mode = os.stat(temp_vault.key_file).st_mode & 0o777
    assert mode == 0o600, f"Expected 0o600, got {oct(mode)}"


def test_vault_creds_file_permissions(temp_vault):
    """Test that credentials file has restricted permissions (0o600)."""
    data = {"LINKEDIN_EMAIL": "test@example.com", "LINKEDIN_PASSWORD": "secret123"}
    temp_vault.encrypt_credentials(data)
    mode = os.stat(temp_vault.creds_file).st_mode & 0o777
    assert mode == 0o600, f"Expected 0o600, got {oct(mode)}"


def test_vault_decrypt_empty_file(temp_vault):
    """Test decrypting when no credentials file exists returns empty dict."""
    result = temp_vault.decrypt_credentials()
    assert result == {}


def test_vault_get_credentials(temp_vault):
    """Test getting credentials as validated model."""
    data = {
        "LINKEDIN_EMAIL": "test@example.com",
        "LINKEDIN_PASSWORD": "secret123",
        "INDEED_EMAIL": "indeed@example.com"
    }
    temp_vault.encrypt_credentials(data)

    creds = temp_vault.get_credentials()
    assert isinstance(creds, Credentials)
    assert creds.linkedin_email == "test@example.com"
    assert creds.indeed_email == "indeed@example.com"


def test_vault_key_rotation(temp_vault):
    """Test key rotation functionality."""
    # Store initial key
    temp_vault._ensure_key()
    initial_key = temp_vault.key_file.read_bytes()

    # Encrypt some data
    data = {"LINKEDIN_EMAIL": "test@example.com", "LINKEDIN_PASSWORD": "secret123"}
    temp_vault.encrypt_credentials(data)

    # Rotate key
    temp_vault.rotate_key()

    # Verify key changed
    new_key = temp_vault.key_file.read_bytes()
    assert new_key != initial_key

    # Verify data still decryptable
    decrypted = temp_vault.decrypt_credentials()
    assert decrypted["LINKEDIN_EMAIL"] == "test@example.com"
    assert decrypted["LINKEDIN_PASSWORD"] == "secret123"


def test_vault_loads_existing_key(temp_vault):
    """Test that vault loads existing key instead of generating new one."""
    # Generate key first
    temp_vault._ensure_key()
    key_content = temp_vault.key_file.read_bytes()

    # Create new vault instance with same key file
    vault2 = CredentialVault(key_file=temp_vault.key_file, creds_file=temp_vault.creds_file)
    vault2._ensure_key()

    # Should use same key
    assert vault2.key_file.read_bytes() == key_content
