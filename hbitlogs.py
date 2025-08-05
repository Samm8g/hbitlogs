import argparse
from db import initialize_db, add_hbit, log_hbit, list_hbits, show_stats, remove_hbit

def main():
    initialize_db()

    parser = argparse.ArgumentParser(prog="hbitlogs", description="Offline CLI Habit Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add habit
    add_parser = subparsers.add_parser("add", help="Add a new habit")
    add_parser.add_argument("name", help="Name of the habit to add")

    # Remove habit
    remove_parser = subparsers.add_parser("remove", help="Remove a habit and its logs")
    remove_parser.add_argument("name", help="Name of the habit to remove")

    # Log habit
    log_parser = subparsers.add_parser("log", help="Log a habit for today")
    log_parser.add_argument("name", help="Name of the habit to log")

    # List habits
    subparsers.add_parser("list", help="List all tracked habits")

    # Show stats
    stats_parser = subparsers.add_parser("stats", help="Show stats for a habit")
    stats_parser.add_argument("name", help="Name of the habit to view stats")

    args = parser.parse_args()

    # Dispatch
    if args.command == "add":
        add_hbit(args.name)
    elif args.command == "log":
        log_hbit(args.name)
    elif args.command == "list":
        list_hbits()
    elif args.command == "stats":
        show_stats(args.name)
    elif args.command == "remove":
        remove_hbit(args.name)

if __name__ == "__main__":
    main()
