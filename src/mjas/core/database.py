"""SQLite database for job tracking and state management."""

import aiosqlite
from pathlib import Path
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass


class JobStatus(str, Enum):
    DISCOVERED = "discovered"
    QUEUED = "queued"
    APPLYING = "applying"
    APPLIED = "applied"
    FAILED = "failed"
    SKIPPED = "skipped"
    INTERVIEW = "interview"


@dataclass
class ApplicationRecord:
    job_id: str
    title: str
    company: str
    portal: str
    url: str
    score: int
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    applied_at: Optional[datetime] = None
    notes: Optional[str] = None


class Database:
    """Async SQLite database manager."""

    def __init__(self, db_path: Path = Path("data/mjas.db")):
        self.db_path = db_path
        self._conn: Optional[aiosqlite.Connection] = None

    async def init(self) -> None:
        """Initialize database and create tables."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = await aiosqlite.connect(self.db_path)
        self._conn.row_factory = aiosqlite.Row
        await self._create_tables()

    async def _create_tables(self) -> None:
        """Create database schema."""
        await self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                portal TEXT NOT NULL,
                url TEXT NOT NULL,
                location TEXT,
                salary_range TEXT,
                description TEXT,
                score INTEGER DEFAULT 0,
                priority TEXT DEFAULT 'MEDIUM',
                status TEXT DEFAULT 'discovered',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                applied_at TIMESTAMP,
                notes TEXT,
                screenshot_path TEXT
            );

            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN NOT NULL,
                error_message TEXT,
                screenshot_path TEXT,
                form_data TEXT,
                FOREIGN KEY (job_id) REFERENCES jobs(job_id)
            );

            CREATE TABLE IF NOT EXISTS portal_stats (
                portal TEXT PRIMARY KEY,
                total_attempts INTEGER DEFAULT 0,
                successful_applications INTEGER DEFAULT 0,
                failed_applications INTEGER DEFAULT 0,
                last_attempt_at TIMESTAMP,
                avg_response_time_ms INTEGER
            );

            CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
            CREATE INDEX IF NOT EXISTS idx_jobs_portal ON jobs(portal);
            CREATE INDEX IF NOT EXISTS idx_jobs_score ON jobs(score DESC);
            CREATE INDEX IF NOT EXISTS idx_jobs_created ON jobs(created_at);
        """)
        await self._conn.commit()

    async def insert_job(
        self,
        job_id: str,
        title: str,
        company: str,
        portal: str,
        url: str,
        score: int = 0,
        priority: str = "MEDIUM",
        location: Optional[str] = None,
        description: Optional[str] = None
    ) -> None:
        """Insert a new job discovery."""
        await self._conn.execute("""
            INSERT OR IGNORE INTO jobs
            (job_id, title, company, portal, url, score, priority, location, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (job_id, title, company, portal, url, score, priority, location, description))
        await self._conn.commit()

    async def update_job_status(
        self,
        job_id: str,
        status: JobStatus,
        notes: Optional[str] = None,
        screenshot_path: Optional[str] = None
    ) -> None:
        """Update job status."""
        applied_at = datetime.now() if status == JobStatus.APPLIED else None

        await self._conn.execute("""
            UPDATE jobs
            SET status = ?, notes = ?, updated_at = ?, applied_at = ?,
                screenshot_path = COALESCE(?, screenshot_path)
            WHERE job_id = ?
        """, (status.value, notes, datetime.now(), applied_at, screenshot_path, job_id))
        await self._conn.commit()

    async def get_job(self, job_id: str) -> Optional[Dict]:
        """Get job by ID."""
        async with self._conn.execute(
            "SELECT * FROM jobs WHERE job_id = ?", (job_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def get_jobs_by_status(
        self,
        status: JobStatus,
        limit: int = 100,
        portal: Optional[str] = None
    ) -> List[Dict]:
        """Get jobs by status, optionally filtered by portal."""
        query = "SELECT * FROM jobs WHERE status = ?"
        params = [status.value]

        if portal:
            query += " AND portal = ?"
            params.append(portal)

        query += " ORDER BY score DESC, created_at DESC LIMIT ?"
        params.append(limit)

        async with self._conn.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def get_priority_queue(self, min_score: int = 65, limit: int = 50) -> List[Dict]:
        """Get high-priority jobs ready for application."""
        async with self._conn.execute("""
            SELECT * FROM jobs
            WHERE status = 'queued' AND score >= ?
            ORDER BY
                CASE priority
                    WHEN 'HIGH' THEN 3
                    WHEN 'MEDIUM' THEN 2
                    ELSE 1
                END DESC,
                score DESC,
                created_at ASC
            LIMIT ?
        """, (min_score, limit)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def log_application_attempt(
        self,
        job_id: str,
        success: bool,
        error_message: Optional[str] = None,
        screenshot_path: Optional[str] = None,
        form_data: Optional[Dict] = None
    ) -> None:
        """Log an application attempt."""
        import json
        await self._conn.execute("""
            INSERT INTO applications
            (job_id, success, error_message, screenshot_path, form_data)
            VALUES (?, ?, ?, ?, ?)
        """, (job_id, success, error_message, screenshot_path,
              json.dumps(form_data) if form_data else None))
        await self._conn.commit()

    async def get_stats(self) -> Dict:
        """Get system statistics."""
        async with self._conn.execute("""
            SELECT
                COUNT(*) as total_jobs,
                SUM(CASE WHEN status = 'applied' THEN 1 ELSE 0 END) as applied,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                SUM(CASE WHEN status = 'queued' THEN 1 ELSE 0 END) as queued,
                AVG(score) as avg_score
            FROM jobs
        """) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else {}

    async def get_portal_stats(self) -> List[Dict]:
        """Get per-portal statistics."""
        async with self._conn.execute("""
            SELECT
                portal,
                COUNT(*) as total,
                SUM(CASE WHEN status = 'applied' THEN 1 ELSE 0 END) as applied,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                AVG(score) as avg_score
            FROM jobs
            GROUP BY portal
            ORDER BY applied DESC
        """) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def close(self) -> None:
        """Close database connection."""
        if self._conn:
            await self._conn.close()
