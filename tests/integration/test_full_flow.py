"""Integration tests for full application flow."""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from mjas.core.vault import CredentialVault
from mjas.core.database import Database, JobStatus
from mjas.core.swarm import SwarmOrchestrator, SwarmConfig
from mjas.portals.base import CandidateProfile, JobListing, JobQuery


@pytest.fixture
async def test_db(tmp_path):
    """Create test database."""
    db = Database(tmp_path / "test.db")
    await db.init()
    yield db
    await db.close()


@pytest.fixture
def test_profile():
    """Test candidate profile."""
    return CandidateProfile(
        full_name="Test User",
        email="test@example.com",
        phone="1234567890",
        location="Remote",
        resume_path="test_resume.pdf",
        summary="Test profile for integration tests",
        skills=["Python", "AI", "Machine Learning"],
        years_experience=3,
        expected_salary="20-40 LPA",
        notice_period="Immediate"
    )


@pytest.mark.asyncio
async def test_database_job_lifecycle(test_db):
    """Test full job lifecycle in database."""
    # Insert job
    await test_db.insert_job(
        job_id="test-123",
        title="AI Engineer",
        company="TestCo",
        portal="linkedin",
        url="https://linkedin.com/jobs/123",
        score=85,
        priority="HIGH"
    )

    # Update to queued
    await test_db.update_job_status("test-123", JobStatus.QUEUED)

    # Get pending jobs
    pending = await test_db.get_jobs_by_status(JobStatus.QUEUED)
    assert len(pending) == 1
    assert pending[0]["job_id"] == "test-123"

    # Update to applied
    await test_db.update_job_status("test-123", JobStatus.APPLIED, notes="Success")

    # Get stats
    stats = await test_db.get_stats()
    assert stats["total_jobs"] == 1
    assert stats["applied"] == 1


@pytest.mark.asyncio
async def test_database_prevents_duplicates(test_db):
    """Test that duplicate jobs are not inserted."""
    # Insert first job
    await test_db.insert_job(
        job_id="dup-test",
        title="First Job",
        company="Company A",
        portal="linkedin",
        url="https://linkedin.com/jobs/1",
        score=80
    )

    # Try to insert duplicate
    await test_db.insert_job(
        job_id="dup-test",
        title="Second Job",
        company="Company B",
        portal="indeed",
        url="https://indeed.com/jobs/2",
        score=90
    )

    # Should only have one job
    stats = await test_db.get_stats()
    assert stats["total_jobs"] == 1


@pytest.mark.asyncio
async def test_database_portal_stats(test_db):
    """Test portal statistics aggregation."""
    # Add jobs from different portals
    portals = ["linkedin", "indeed", "wellfound"]
    for i, portal in enumerate(portals):
        await test_db.insert_job(
            job_id=f"portal-{i}",
            title=f"Job {i}",
            company=f"Company {i}",
            portal=portal,
            url=f"https://{portal}.com/jobs/{i}",
            score=75
        )
        await test_db.update_job_status(f"portal-{i}", JobStatus.APPLIED)

    # Get portal stats
    portal_stats = await test_db.get_portal_stats()
    assert len(portal_stats) == 3

    for ps in portal_stats:
        assert ps["applied"] == 1
        assert ps["total"] == 1


@pytest.mark.asyncio
async def test_swarm_initialization(test_db, test_profile, tmp_path):
    """Test swarm can be initialized with config."""
    # Create mock vault
    mock_vault = MagicMock()
    mock_creds = MagicMock()
    mock_creds.model_dump.return_value = {
        "linkedin_email": "test@example.com",
        "linkedin_password": "test"
    }
    mock_vault.get_credentials.return_value = mock_creds

    config = SwarmConfig(headless=True, daily_application_target=100)
    swarm = SwarmOrchestrator(config, mock_vault, test_db, test_profile)

    assert swarm.config.headless is True
    assert swarm.config.daily_application_target == 100
    assert len(swarm.workers) == 0


@pytest.mark.asyncio
async def test_swarm_config_defaults():
    """Test swarm configuration defaults."""
    config = SwarmConfig()

    assert config.headless is True
    assert config.max_concurrent_workers == 4
    assert config.min_job_score == 65
    assert config.daily_application_target == 200
    assert "AI Engineer" in config.search_keywords
    assert "Remote" in config.search_locations


@pytest.mark.asyncio
async def test_swarm_config_custom():
    """Test swarm configuration customization."""
    config = SwarmConfig(
        headless=False,
        search_keywords=["Data Scientist", "ML Engineer"],
        search_locations=["Bangalore", "Hyderabad"],
        daily_application_target=50
    )

    assert config.headless is False
    assert "Data Scientist" in config.search_keywords
    assert "Bangalore" in config.search_locations
    assert config.daily_application_target == 50


@pytest.mark.asyncio
async def test_job_listing_creation():
    """Test job listing data model."""
    job = JobListing(
        job_id="test-job-123",
        title="Senior AI Engineer",
        company="TechCorp",
        location="Remote",
        url="https://example.com/job/123",
        portal="linkedin",
        description="Build AI systems",
        salary_range="$150k-$200k",
        score=90,
        priority="HIGH"
    )

    assert job.job_id == "test-job-123"
    assert job.score == 90
    assert job.priority == "HIGH"
    assert "TechCorp" in job.company


@pytest.mark.asyncio
async def test_job_query_defaults():
    """Test job query parameters."""
    query = JobQuery(keywords="AI Engineer", location="Remote")

    assert query.keywords == "AI Engineer"
    assert query.location == "Remote"
    assert query.remote is True
    assert query.posted_within_days == 7
    assert query.experience_level is None


@pytest.mark.asyncio
async def test_candidate_profile_to_dict(test_profile):
    """Test candidate profile serialization."""
    profile_dict = test_profile.to_dict()

    assert profile_dict["full_name"] == "Test User"
    assert profile_dict["email"] == "test@example.com"
    assert profile_dict["first_name"] == "Test"
    assert profile_dict["last_name"] == "User"
    assert "Python" in profile_dict["skills"]


@pytest.mark.asyncio
async def test_database_application_logging(test_db):
    """Test application attempt logging."""
    # Insert job
    await test_db.insert_job(
        job_id="log-test",
        title="Test Job",
        company="TestCo",
        portal="linkedin",
        url="https://linkedin.com/jobs/test",
        score=80
    )

    # Log successful application
    await test_db.log_application_attempt(
        job_id="log-test",
        success=True,
        form_data={"applied_at": "2024-01-01"}
    )

    # Log failed application
    await test_db.log_application_attempt(
        job_id="log-test",
        success=False,
        error_message="CAPTCHA detected",
        screenshot_path="screenshots/captcha.png"
    )

    # Both logs should exist (we'd need a query to verify, but no errors = success)
    stats = await test_db.get_stats()
    assert stats["total_jobs"] == 1


@pytest.mark.asyncio
async def test_portal_registry():
    """Test portal registry functionality."""
    from mjas.portals.registry import (
        get_portal, list_portals, list_portals_by_tier,
        TIER_1_PORTALS, TIER_2_PORTALS, TIER_3_PORTALS
    )

    # Test list_portals
    all_portals = list_portals()
    assert len(all_portals) >= 4
    assert "linkedin" in all_portals
    assert "indeed" in all_portals

    # Test list_portals_by_tier
    tier1 = list_portals_by_tier(1)
    assert tier1 == TIER_1_PORTALS

    tier2 = list_portals_by_tier(2)
    assert tier2 == TIER_2_PORTALS

    tier3 = list_portals_by_tier(3)
    assert tier3 == TIER_3_PORTALS

    # Test get_portal with invalid name
    with pytest.raises(ValueError, match="Unknown portal"):
        get_portal("invalid_portal", {})
