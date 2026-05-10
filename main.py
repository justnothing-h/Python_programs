"""
main.py
Unified entry point for the GitHub Contribution Bot.

Usage:
    python main.py                  → Launch GUI dashboard
    python main.py commit           → Run one commit cycle now
    python main.py commit --count 3 → Run 3 commits
    python main.py schedule         → Start the scheduler daemon
    python main.py generate         → Generate a file (no commit)
    python main.py status           → Show repo status
    python main.py setup            → Interactive first-time setup
"""

import argparse
import os
import sys

# Ensure package root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import get_logger
from utils.config_loader import load_config, save_config

logger = get_logger("main")


def cmd_commit(args):
    from auto_commit import run_multiple_commits
    cfg = load_config()
    n = args.count if hasattr(args, "count") and args.count else cfg.get("commits_per_day", 1)
    logger.info(f"Running {n} commit(s)...")
    done = run_multiple_commits(n, cfg)
    print(f"\n✓ Completed {done}/{n} commits.")


def cmd_schedule(args):
    from scheduler import GitBotScheduler
    cfg = load_config()
    bot = GitBotScheduler(cfg)
    print("Starting scheduler... Press Ctrl+C to stop.\n")
    bot.start()


def cmd_generate(args):
    from generator import generate_file
    cfg = load_config()
    repo_path = os.path.abspath(cfg.get("repo_path", "./repo"))
    path = generate_file(repo_path, cfg)
    if path:
        print(f"✓ Generated: {path}")
    else:
        print("✗ Generation failed. Check logs.")


def cmd_status(args):
    from auto_commit import ensure_repo, get_commit_count, get_recent_commits, get_current_branch
    cfg = load_config()
    repo_path = ensure_repo(cfg)
    if not repo_path:
        print("✗ Repo not set up.")
        return

    branch = get_current_branch(repo_path)
    total = get_commit_count(repo_path)
    recent = get_recent_commits(repo_path, 5)

    print(f"\n{'─'*50}")
    print(f"  GitHub Contribution Bot — Status")
    print(f"{'─'*50}")
    print(f"  Repo:    {repo_path}")
    print(f"  Branch:  {branch}")
    print(f"  Commits: {total}")
    print(f"  Remote:  {cfg.get('remote_url') or '(not set)'}")
    print(f"\n  Recent commits:")
    for c in recent:
        print(f"    [{c['date']}] {c['hash']}  {c['message'][:55]}")
    print(f"{'─'*50}\n")


def cmd_setup(args):
    """Interactive first-time setup wizard."""
    cfg = load_config()
    print("\n" + "="*55)
    print("  GitHub Contribution Bot — Setup Wizard")
    print("="*55 + "\n")

    fields = [
        ("repo_path", "Repo path (default ./repo)", "./repo"),
        ("remote_url", "GitHub remote URL (leave blank to skip push)", ""),
        ("branch", "Branch name", "main"),
        ("author_name", "Git author name", "GitHub Bot"),
        ("author_email", "Git author email", "bot@example.com"),
        ("commits_per_day", "Commits per day", "2"),
        ("schedule_time", "Default schedule time (HH:MM)", "11:00"),
    ]

    for key, prompt, default in fields:
        current = str(cfg.get(key, default))
        val = input(f"  {prompt} [{current}]: ").strip()
        if val:
            cfg[key] = int(val) if key == "commits_per_day" else val

    auto_push = input("  Auto push to GitHub? (y/n) [y]: ").strip().lower()
    cfg["auto_push"] = auto_push != "n"

    if save_config(cfg):
        print("\n✓ Config saved to config.json")
    else:
        print("\n✗ Failed to save config.")

    # Init repo
    from auto_commit import ensure_repo
    repo = ensure_repo(cfg)
    if repo:
        print(f"✓ Repo ready at: {repo}")
    else:
        print("✗ Could not initialize repo.")

    print("\nSetup complete! Run: python main.py commit\n")


def cmd_gui(args):
    from gui.dashboard import launch
    launch()


def main():
    parser = argparse.ArgumentParser(
        prog="github-bot",
        description="GitHub Contribution Bot",
    )
    subparsers = parser.add_subparsers(dest="command")

    # commit
    p_commit = subparsers.add_parser("commit", help="Run commit cycle(s)")
    p_commit.add_argument("--count", "-n", type=int, default=None, help="Number of commits")
    p_commit.set_defaults(func=cmd_commit)

    # schedule
    p_sched = subparsers.add_parser("schedule", help="Start the scheduler daemon")
    p_sched.set_defaults(func=cmd_schedule)

    # generate
    p_gen = subparsers.add_parser("generate", help="Generate a file without committing")
    p_gen.set_defaults(func=cmd_generate)

    # status
    p_status = subparsers.add_parser("status", help="Show repo and commit stats")
    p_status.set_defaults(func=cmd_status)

    # setup
    p_setup = subparsers.add_parser("setup", help="Interactive first-time setup")
    p_setup.set_defaults(func=cmd_setup)

    # gui
    p_gui = subparsers.add_parser("gui", help="Launch the GUI dashboard")
    p_gui.set_defaults(func=cmd_gui)

    args = parser.parse_args()

    if args.command is None:
        # Default: launch GUI, fall back to status if no display
        try:
            cmd_gui(args)
        except Exception as e:
            logger.warning(f"GUI unavailable ({e}), showing status instead.")
            cmd_status(args)
    else:
        args.func(args)


if __name__ == "__main__":
    main()
