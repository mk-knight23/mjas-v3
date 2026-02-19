"""MJAS v3.0 - Main entry point."""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

from mjas.core.database import Database
from mjas.core.swarm import SwarmConfig, SwarmOrchestrator
from mjas.core.session_manager import SessionManager
from mjas.portals.base import CandidateProfile
from mjas.portals.registry import (
    NO_LOGIN_PORTALS,
    TECH_PORTALS,
    TIER_1_PORTALS,
    TIER_2_PORTALS,
    TIER_3_PORTALS,
)


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/mjas.log')
        ]
    )


def load_candidate_profile() -> CandidateProfile:
    """Load candidate profile from config."""
    return CandidateProfile(
        full_name="Musharraf Kazi",
        email="kazimusharraf1234@gmail.com",
        phone="+919765490536",
        location="India",
        linkedin_url="https://www.linkedin.com/in/kazi-musharraf-0674871a4",
        github_url="https://github.com/mk-knight23",
        portfolio_url="",
        resume_path="config/musharraf_kazi_resume.pdf",
        summary="AI Engineer and Indie Builder specializing in Agentic AI Systems and Multi-LLM orchestration. Builder of VIBE.",
        skills=["Python", "LangChain", "LangGraph", "FastAPI", "OpenAI API", "RAG", "Multi-Agent Systems", "Next.js"],
        years_experience=3,
        expected_salary="20-40 LPA",
        notice_period="Immediate",
        work_authorization="Authorized to work in India"
    )


async def cmd_setup(args):
    """Initialize system (database only)."""
    print("MJAS v3.0 Setup")
    print("=" * 40)
    print()

    # Initialize database
    db = Database()
    await db.init()
    print(f"Database initialized at: {db.db_path}")
    await db.close()

    print()
    print("Next: Setup browser sessions with Google Sign-In")
    print("  python -m mjas setup-sessions")

    return 0


async def cmd_run(args):
    """Run full cycle."""
    setup_logging(args.verbose)

    db = Database()
    await db.init()

    session_mgr = SessionManager()
    profile = load_candidate_profile()
    config = SwarmConfig(
        headless=not args.visible,
        daily_application_target=args.target
    )

    swarm = SwarmOrchestrator(config, db, profile, session_mgr)
    await swarm.initialize_workers(args.portals, tier=args.tier)

    if not swarm.workers:
        print("ERROR: No workers initialized. Check session setup.")
        return 1

    if args.continuous:
        await swarm.continuous_mode(interval_minutes=args.interval)
    else:
        stats = await swarm.run_full_cycle()
        print("\n=== Results ===")
        print(f"Jobs discovered: {stats['research']}")
        print(f"Jobs applied: {stats['applied']}")
        print(f"Total in database: {stats.get('total_jobs', 0)}")

    await swarm.shutdown()
    await db.close()
    return 0


async def cmd_list_portals(args):
    """List available job portals."""
    print("\n=== MJAS Job Portals ===\n")

    print("Tier 1 (Major Platforms):")
    for portal in TIER_1_PORTALS:
        marker = "🌐" if portal in NO_LOGIN_PORTALS else "🔐"
        tech = " [Tech]" if portal in TECH_PORTALS else ""
        print(f"  {marker} {portal}{tech}")

    print("\nTier 2 (Secondary Platforms):")
    for portal in TIER_2_PORTALS:
        marker = "🌐" if portal in NO_LOGIN_PORTALS else "🔐"
        tech = " [Tech]" if portal in TECH_PORTALS else ""
        print(f"  {marker} {portal}{tech}")

    print("\nTier 3 (Specialized/Curated):")
    for portal in TIER_3_PORTALS:
        marker = "🌐" if portal in NO_LOGIN_PORTALS else "🔐"
        tech = " [Tech]" if portal in TECH_PORTALS else ""
        print(f"  {marker} {portal}{tech}")

    print("\n=== Legend ===")
    print("  🔐 = Requires login")
    print("  🌐 = No login required")
    print("  [Tech] = AI/Tech focused portal")
    print("\n=== Usage ===")
    print("  python -m mjas run --tier 1      # Use Tier 1 portals only")
    print("  python -m mjas run --tier 2      # Use Tier 2 portals only")
    print("  python -m mjas run --tier 3      # Use Tier 3 portals only")
    print("  python -m mjas run --portals linkedin indeed  # Use specific portals")
    print()

    return 0


async def cmd_stats(args):
    """Show statistics."""
    db = Database()
    await db.init()

    stats = await db.get_stats()
    portal_stats = await db.get_portal_stats()

    print("\n=== MJAS Statistics ===")
    print(f"Total jobs tracked: {stats.get('total_jobs', 0)}")
    print(f"Successfully applied: {stats.get('applied', 0)}")
    print(f"Failed: {stats.get('failed', 0)}")
    print(f"Queued: {stats.get('queued', 0)}")
    avg_score = stats.get('avg_score') or 0
    print(f"Average score: {avg_score:.1f}")

    if portal_stats:
        print("\n=== By Portal ===")
        for ps in portal_stats:
            print(f"  {ps['portal']}: {ps['applied']} applied, {ps['failed']} failed")

    await db.close()
    return 0


async def cmd_setup_sessions(args):
    """Interactive session setup with Google Sign-In."""
    from playwright.async_api import async_playwright
    from mjas.core.session_manager import SessionManager
    from mjas.portals.registry import TIER_1_PORTALS, TIER_2_PORTALS

    portal_urls = {
        "linkedin": "https://www.linkedin.com/login",
        "indeed": "https://secure.indeed.com/account/login",
        "wellfound": "https://wellfound.com/login",
        "naukri": "https://www.naukri.com/nlogin/login",
        "glassdoor": "https://www.glassdoor.com/profile/login_input.htm",
        "ziprecruiter": "https://www.ziprecruiter.com/auth/login",
        "dice": "https://www.dice.com/dashboard/login"
    }

    print("\n" + "=" * 60)
    print("MJAS Session Setup with Google Sign-In")
    print("=" * 60)
    print("\nUse Gmail: kazimusharraf1234@gmail.com")
    print("\nFor each portal:")
    print("  1. Click 'Sign in with Google'")
    print("  2. Sign in with your Gmail")
    print("  3. Complete any 2FA/security checks")
    print("  4. Wait for 'Session saved!' message")
    print("\nPress Ctrl+C to skip a portal.")
    print("=" * 60 + "\n")

    session_mgr = SessionManager()
    portals = TIER_1_PORTALS + TIER_2_PORTALS

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        for portal in portals:
            if portal not in portal_urls:
                continue

            # Skip if session exists and no --force flag
            if session_mgr.session_exists(portal) and not args.force:
                print(f"[{portal}] Session already exists (use --force to overwrite)")
                continue

            print(f"\n[{portal}] Opening login page...")
            print(f"[{portal}] Please click 'Sign in with Google' and complete login.")

            context = await browser.new_context()
            page = await context.new_page()

            try:
                await page.goto(portal_urls[portal])

                # Wait for user to complete login (up to 5 minutes)
                print(f"[{portal}] Waiting for login (press Ctrl+C to skip)...")

                # Wait for URL change or specific element that indicates logged in state
                # We'll wait for user to press Enter when done
                print(f"[{portal}] Press Enter when you've completed login (or Ctrl+C to skip): ", end="", flush=True)

                # Use asyncio to wait for user input without blocking the browser
                import asyncio
                try:
                    # Wait for user input with a timeout
                    await asyncio.wait_for(
                        asyncio.get_event_loop().run_in_executor(None, input),
                        timeout=300  # 5 minutes
                    )
                except asyncio.TimeoutError:
                    print(f"\n[{portal}] Timeout - skipping.")
                    await context.close()
                    continue

                # Save session
                storage_state = await context.storage_state()
                session_mgr.save_session(portal, storage_state)
                print(f"[{portal}] Session saved!")

            except KeyboardInterrupt:
                print(f"\n[{portal}] Skipped by user.")
            except Exception as e:
                print(f"\n[{portal}] Error: {e}")
            finally:
                try:
                    await context.close()
                except Exception:
                    pass

        await browser.close()

    print("\n" + "=" * 60)
    print("Session setup complete!")
    print("Saved sessions: " + ", ".join(session_mgr.list_sessions()))
    print("=" * 60)
    return 0


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="MJAS v3.0 - Mikazi Job Application Swarm",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m mjas setup                    # Initialize database
  python -m mjas setup-sessions           # Setup browser sessions
  python -m mjas run                      # Run one full cycle
  python -m mjas run --continuous         # Run continuously
  python -m mjas run --visible            # Show browser window
  python -m mjas stats                    # Show statistics
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Setup command
    subparsers.add_parser('setup', help='Initialize system')

    # Run command
    run_parser = subparsers.add_parser('run', help='Run full cycle')
    run_parser.add_argument('--portals', nargs='+', help='Specific portals to use')
    run_parser.add_argument('--tier', type=int, choices=[1, 2, 3], help='Portal tier (1=major, 2=secondary, 3=specialized)')
    run_parser.add_argument('--visible', action='store_true', help='Show browser window')
    run_parser.add_argument('--continuous', action='store_true', help='Run continuously')
    run_parser.add_argument('--interval', type=int, default=120, help='Minutes between cycles')
    run_parser.add_argument('--target', type=int, default=200, help='Daily application target')
    run_parser.add_argument('-v', '--verbose', action='store_true')

    # Stats command
    subparsers.add_parser('stats', help='Show statistics')

    # List portals command
    subparsers.add_parser('list-portals', help='List available job portals')

    # Setup sessions command
    setup_sessions_parser = subparsers.add_parser('setup-sessions', help='Setup browser sessions with Google Sign-In')
    setup_sessions_parser.add_argument('--force', action='store_true', help='Overwrite existing sessions')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Ensure directories exist
    Path("logs").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    Path("config").mkdir(exist_ok=True)

    # Route to command handler
    handlers = {
        'setup': cmd_setup,
        'run': cmd_run,
        'stats': cmd_stats,
        'list-portals': cmd_list_portals,
        'setup-sessions': cmd_setup_sessions,
    }

    handler = handlers.get(args.command)
    if handler:
        return await handler(args)

    return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
