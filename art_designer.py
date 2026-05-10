"""
art_designer.py
Helper to design contribution art patterns.
Define pixel-art letters/shapes on a 7-row grid and convert them
to the YYYY-MM-DD:N format that the scheduler understands.

Usage:
    python art_designer.py --text "HI" --start 2025-06-01
    python art_designer.py --preview
"""

import argparse
from datetime import date, timedelta
import json

# 5-wide pixel font for A-Z, 0-9 and space
PIXEL_FONT = {
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'B': ["11110","10001","10001","11110","10001","10001","11110"],
    'C': ["01110","10001","10000","10000","10000","10001","01110"],
    'D': ["11110","10001","10001","10001","10001","10001","11110"],
    'E': ["11111","10000","10000","11110","10000","10000","11111"],
    'F': ["11111","10000","10000","11110","10000","10000","10000"],
    'G': ["01110","10001","10000","10111","10001","10001","01111"],
    'H': ["10001","10001","10001","11111","10001","10001","10001"],
    'I': ["11111","00100","00100","00100","00100","00100","11111"],
    'J': ["00111","00010","00010","00010","10010","10010","01100"],
    'K': ["10001","10010","10100","11000","10100","10010","10001"],
    'L': ["10000","10000","10000","10000","10000","10000","11111"],
    'M': ["10001","11011","10101","10001","10001","10001","10001"],
    'N': ["10001","11001","10101","10011","10001","10001","10001"],
    'O': ["01110","10001","10001","10001","10001","10001","01110"],
    'P': ["11110","10001","10001","11110","10000","10000","10000"],
    'Q': ["01110","10001","10001","10001","10101","10010","01101"],
    'R': ["11110","10001","10001","11110","10100","10010","10001"],
    'S': ["01111","10000","10000","01110","00001","00001","11110"],
    'T': ["11111","00100","00100","00100","00100","00100","00100"],
    'U': ["10001","10001","10001","10001","10001","10001","01110"],
    'V': ["10001","10001","10001","10001","10001","01010","00100"],
    'W': ["10001","10001","10001","10101","10101","11011","10001"],
    'X': ["10001","10001","01010","00100","01010","10001","10001"],
    'Y': ["10001","10001","01010","00100","00100","00100","00100"],
    'Z': ["11111","00001","00010","00100","01000","10000","11111"],
    '0': ["01110","10001","10011","10101","11001","10001","01110"],
    '1': ["00100","01100","00100","00100","00100","00100","01110"],
    '2': ["01110","10001","00001","00110","01000","10000","11111"],
    '3': ["11110","00001","00001","01110","00001","00001","11110"],
    '4': ["00010","00110","01010","10010","11111","00010","00010"],
    '5': ["11111","10000","10000","11110","00001","00001","11110"],
    '6': ["01110","10000","10000","11110","10001","10001","01110"],
    '7': ["11111","00001","00010","00100","01000","01000","01000"],
    '8': ["01110","10001","10001","01110","10001","10001","01110"],
    '9': ["01110","10001","10001","01111","00001","00001","01110"],
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
    '!': ["00100","00100","00100","00100","00100","00000","00100"],
}


def text_to_grid(text: str) -> list:
    """Convert text to a 7×N boolean grid."""
    text = text.upper()
    cols = []
    for i, ch in enumerate(text):
        glyph = PIXEL_FONT.get(ch, PIXEL_FONT[' '])
        for col in range(5):
            cols.append([int(row[col]) for row in glyph])
        if i < len(text) - 1:
            cols.append([0] * 7)  # 1-px gap between letters
    return cols  # list of 7-item columns


def grid_to_schedule(cols: list, start: date, intensity: int = 4) -> list:
    """
    Map grid columns to weeks starting from `start` (a Sunday).
    Returns list of 'YYYY-MM-DD:N' strings.
    """
    # GitHub graph: columns = weeks (Sunday=row 0 … Saturday=row 6)
    entries = []
    for week_idx, col in enumerate(cols):
        for day_idx, filled in enumerate(col):
            if filled:
                d = start + timedelta(weeks=week_idx, days=day_idx)
                entries.append(f"{d.isoformat()}:{intensity}")
    return entries


def next_sunday(from_date: date = None) -> date:
    d = from_date or date.today()
    days_ahead = (6 - d.weekday()) % 7  # weekday: Mon=0 Sun=6
    return d + timedelta(days=days_ahead + 1)


def preview_grid(cols: list):
    """Print ASCII art preview of the grid."""
    rows = 7
    print("\n  Preview:")
    for r in range(rows):
        line = "  "
        for col in cols:
            line += "██" if col[r] else "  "
        print(line)
    print()


def main():
    parser = argparse.ArgumentParser(description="Contribution art pattern designer")
    parser.add_argument("--text", "-t", default="HI", help="Text to render (A-Z, 0-9, space, !)")
    parser.add_argument("--start", "-s", default="", help="Start date YYYY-MM-DD (default: next Sunday)")
    parser.add_argument("--intensity", "-i", type=int, default=4, choices=[1, 2, 3, 4],
                        help="Commit intensity (1=light, 4=darkest)")
    parser.add_argument("--preview", "-p", action="store_true", help="Show ASCII preview only")
    parser.add_argument("--output", "-o", default="", help="Append to config.json automatically")
    args = parser.parse_args()

    cols = text_to_grid(args.text)
    preview_grid(cols)

    if args.preview:
        return

    start_date = date.fromisoformat(args.start) if args.start else next_sunday()
    print(f"  Start date: {start_date} (week {start_date.strftime('%A')})")
    print(f"  Width:      {len(cols)} weeks needed\n")

    schedule = grid_to_schedule(cols, start_date, args.intensity)
    print("  Schedule entries:")
    for e in schedule[:20]:
        print(f"    {e}")
    if len(schedule) > 20:
        print(f"    ... ({len(schedule) - 20} more)")
    print()

    if args.output or input("  Add to config.json? (y/n): ").strip().lower() == "y":
        import os
        cfg_path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(cfg_path, "r") as f:
            cfg = json.load(f)
        cfg.setdefault("scheduler", {})["contribution_art"] = schedule
        cfg["scheduler"]["mode"] = "art"
        with open(cfg_path, "w") as f:
            json.dump(cfg, f, indent=2)
        print("  ✓ Written to config.json  (mode set to 'art')")


if __name__ == "__main__":
    main()
