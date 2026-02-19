"""Unit tests for the SessionManager class."""

import json
import os
import pytest
from pathlib import Path

from mjas.core.session_manager import SessionManager


@pytest.fixture
def temp_session_manager(tmp_path):
    """Create a temporary session manager for testing."""
    session_dir = tmp_path / "sessions"
    return SessionManager(session_dir=session_dir)


class TestSessionManagerInit:
    """Tests for SessionManager initialization."""

    def test_init_creates_directory(self, tmp_path):
        """Test that init creates the session directory."""
        session_dir = tmp_path / "new_sessions"
        assert not session_dir.exists()
        SessionManager(session_dir=session_dir)
        assert session_dir.exists()

    def test_init_uses_existing_directory(self, tmp_path):
        """Test that init works with existing directory."""
        session_dir = tmp_path / "existing_sessions"
        session_dir.mkdir()
        manager = SessionManager(session_dir=session_dir)
        assert manager.session_dir == session_dir

    def test_default_session_dir(self):
        """Test that default session dir is data/sessions."""
        manager = SessionManager()
        assert manager.session_dir == Path("data/sessions")


class TestGetSessionPath:
    """Tests for get_session_path method."""

    def test_get_session_path(self, temp_session_manager):
        """Test getting session path for a portal."""
        path = temp_session_manager.get_session_path("linkedin")
        expected = temp_session_manager.session_dir / "linkedin.json"
        assert path == expected

    def test_get_session_path_different_portals(self, temp_session_manager):
        """Test getting session paths for different portals."""
        linkedin_path = temp_session_manager.get_session_path("linkedin")
        indeed_path = temp_session_manager.get_session_path("indeed")

        assert linkedin_path.name == "linkedin.json"
        assert indeed_path.name == "indeed.json"
        assert linkedin_path != indeed_path


class TestSessionExists:
    """Tests for session_exists method."""

    def test_session_exists_returns_true(self, temp_session_manager):
        """Test that session_exists returns True when file exists."""
        session_file = temp_session_manager.get_session_path("linkedin")
        session_file.write_text("{}")
        assert temp_session_manager.session_exists("linkedin") is True

    def test_session_exists_returns_false(self, temp_session_manager):
        """Test that session_exists returns False when file doesn't exist."""
        assert temp_session_manager.session_exists("nonexistent") is False


class TestSaveSession:
    """Tests for save_session method."""

    def test_save_session_creates_file(self, temp_session_manager):
        """Test that save_session creates a JSON file."""
        data = {"cookies": [{"name": "session", "value": "abc123"}]}
        temp_session_manager.save_session("linkedin", data)

        session_file = temp_session_manager.get_session_path("linkedin")
        assert session_file.exists()

    def test_save_session_writes_valid_json(self, temp_session_manager):
        """Test that save_session writes valid JSON."""
        data = {"cookies": [{"name": "session", "value": "abc123"}]}
        temp_session_manager.save_session("linkedin", data)

        session_file = temp_session_manager.get_session_path("linkedin")
        loaded = json.loads(session_file.read_text())
        assert loaded == data

    def test_save_session_file_permissions(self, temp_session_manager):
        """Test that saved session file has restricted permissions (0o600)."""
        data = {"cookies": [{"name": "session", "value": "abc123"}]}
        temp_session_manager.save_session("linkedin", data)

        session_file = temp_session_manager.get_session_path("linkedin")
        mode = os.stat(session_file).st_mode & 0o777
        assert mode == 0o600, f"Expected 0o600, got {oct(mode)}"

    def test_save_session_overwrites_existing(self, temp_session_manager):
        """Test that save_session overwrites existing session."""
        old_data = {"cookies": [{"name": "old", "value": "old123"}]}
        new_data = {"cookies": [{"name": "new", "value": "new456"}]}

        temp_session_manager.save_session("linkedin", old_data)
        temp_session_manager.save_session("linkedin", new_data)

        loaded = temp_session_manager.load_session("linkedin")
        assert loaded == new_data

    def test_save_session_with_complex_data(self, temp_session_manager):
        """Test saving complex session data."""
        data = {
            "cookies": [
                {"name": "li_at", "value": "token123", "domain": ".linkedin.com"},
                {"name": "JSESSIONID", "value": "session456", "domain": "www.linkedin.com"}
            ],
            "localStorage": {
                "userId": "12345",
                "settings": {"theme": "dark"}
            },
            "timestamp": "2024-01-15T10:30:00"
        }
        temp_session_manager.save_session("linkedin", data)

        loaded = temp_session_manager.load_session("linkedin")
        assert loaded == data


class TestLoadSession:
    """Tests for load_session method."""

    def test_load_session_returns_data(self, temp_session_manager):
        """Test loading an existing session."""
        data = {"cookies": [{"name": "session", "value": "abc123"}]}
        temp_session_manager.save_session("linkedin", data)

        loaded = temp_session_manager.load_session("linkedin")
        assert loaded == data

    def test_load_session_returns_none_for_missing(self, temp_session_manager):
        """Test that load_session returns None for non-existent session."""
        result = temp_session_manager.load_session("nonexistent")
        assert result is None

    def test_load_session_handles_invalid_json(self, temp_session_manager):
        """Test that load_session handles invalid JSON gracefully."""
        session_file = temp_session_manager.get_session_path("linkedin")
        session_file.write_text("not valid json")

        result = temp_session_manager.load_session("linkedin")
        assert result is None

    def test_load_session_handles_empty_file(self, temp_session_manager):
        """Test that load_session handles empty file gracefully."""
        session_file = temp_session_manager.get_session_path("linkedin")
        session_file.write_text("")

        result = temp_session_manager.load_session("linkedin")
        assert result is None


class TestDeleteSession:
    """Tests for delete_session method."""

    def test_delete_session_removes_file(self, temp_session_manager):
        """Test that delete_session removes the session file."""
        data = {"cookies": []}
        temp_session_manager.save_session("linkedin", data)

        assert temp_session_manager.session_exists("linkedin")
        temp_session_manager.delete_session("linkedin")
        assert not temp_session_manager.session_exists("linkedin")

    def test_delete_session_returns_true_on_success(self, temp_session_manager):
        """Test that delete_session returns True when file is deleted."""
        data = {"cookies": []}
        temp_session_manager.save_session("linkedin", data)

        result = temp_session_manager.delete_session("linkedin")
        assert result is True

    def test_delete_session_returns_false_for_missing(self, temp_session_manager):
        """Test that delete_session returns False for non-existent session."""
        result = temp_session_manager.delete_session("nonexistent")
        assert result is False


class TestListSessions:
    """Tests for list_sessions method."""

    def test_list_sessions_empty(self, temp_session_manager):
        """Test that list_sessions returns empty list when no sessions."""
        sessions = temp_session_manager.list_sessions()
        assert sessions == []

    def test_list_sessions_returns_portal_names(self, temp_session_manager):
        """Test that list_sessions returns portal names without extension."""
        temp_session_manager.save_session("linkedin", {"cookies": []})
        temp_session_manager.save_session("indeed", {"cookies": []})
        temp_session_manager.save_session("wellfound", {"cookies": []})

        sessions = temp_session_manager.list_sessions()
        assert sessions == ["indeed", "linkedin", "wellfound"]

    def test_list_sessions_sorted(self, temp_session_manager):
        """Test that list_sessions returns sorted portal names."""
        temp_session_manager.save_session("zebra", {"cookies": []})
        temp_session_manager.save_session("alpha", {"cookies": []})
        temp_session_manager.save_session("beta", {"cookies": []})

        sessions = temp_session_manager.list_sessions()
        assert sessions == ["alpha", "beta", "zebra"]

    def test_list_sessions_ignores_non_json_files(self, temp_session_manager):
        """Test that list_sessions ignores non-JSON files."""
        temp_session_manager.save_session("linkedin", {"cookies": []})

        # Create a non-JSON file
        other_file = temp_session_manager.session_dir / "readme.txt"
        other_file.write_text("This is not a session")

        sessions = temp_session_manager.list_sessions()
        assert sessions == ["linkedin"]

    def test_list_sessions_handles_missing_directory(self, tmp_path):
        """Test that list_sessions handles missing directory gracefully."""
        session_dir = tmp_path / "nonexistent"
        manager = SessionManager(session_dir=session_dir)

        # Delete the directory after creation
        import shutil
        shutil.rmtree(session_dir)

        sessions = manager.list_sessions()
        assert sessions == []
