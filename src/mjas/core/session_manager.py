"""Session persistence for browser contexts."""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages browser session persistence."""

    def __init__(self, session_dir: Path = Path("data/sessions")):
        """Initialize the session manager.

        Args:
            session_dir: Directory to store session files.
        """
        self.session_dir = session_dir
        self.session_dir.mkdir(parents=True, exist_ok=True)

    def get_session_path(self, portal: str) -> Path:
        """Get the file path for a portal's session.

        Args:
            portal: The portal name (e.g., 'linkedin', 'indeed').

        Returns:
            Path to the session JSON file.
        """
        return self.session_dir / f"{portal}.json"

    def session_exists(self, portal: str) -> bool:
        """Check if a session exists for the given portal.

        Args:
            portal: The portal name.

        Returns:
            True if the session file exists, False otherwise.
        """
        return self.get_session_path(portal).exists()

    def save_session(self, portal: str, context_data: Dict[str, Any]) -> None:
        """Save a browser session to JSON file.

        Args:
            portal: The portal name.
            context_data: The session data to save (e.g., cookies, localStorage).
        """
        session_path = self.get_session_path(portal)
        try:
            session_path.write_text(
                json.dumps(context_data, indent=2, default=str),
                encoding="utf-8"
            )
            os.chmod(session_path, 0o600)  # User read/write only
            logger.info(f"Session saved for {portal} at {session_path}")
        except (OSError, TypeError) as e:
            logger.error(f"Failed to save session for {portal}: {e}")
            raise

    def load_session(self, portal: str) -> Optional[Dict[str, Any]]:
        """Load a browser session from JSON file.

        Args:
            portal: The portal name.

        Returns:
            The session data if found, None otherwise.
        """
        session_path = self.get_session_path(portal)
        if not session_path.exists():
            logger.debug(f"No session found for {portal}")
            return None

        try:
            data = json.loads(session_path.read_text(encoding="utf-8"))
            logger.info(f"Session loaded for {portal} from {session_path}")
            return data
        except (OSError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load session for {portal}: {e}")
            return None

    def delete_session(self, portal: str) -> bool:
        """Delete a session file for the given portal.

        Args:
            portal: The portal name.

        Returns:
            True if the session was deleted, False if it didn't exist.
        """
        session_path = self.get_session_path(portal)
        if session_path.exists():
            try:
                session_path.unlink()
                logger.info(f"Session deleted for {portal}")
                return True
            except OSError as e:
                logger.error(f"Failed to delete session for {portal}: {e}")
                raise
        return False

    def list_sessions(self) -> list[str]:
        """List all saved session portal names.

        Returns:
            List of portal names with saved sessions.
        """
        if not self.session_dir.exists():
            return []

        sessions = []
        for file_path in self.session_dir.glob("*.json"):
            sessions.append(file_path.stem)
        return sorted(sessions)
