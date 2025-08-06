# 🗓️ HBitLogs

**⚠️ PROJECT FROZEN ⚠️**

This repository is currently frozen until further notice due to ongoing technical challenges with the GTK 4 GUI implementation. Development will resume when these issues are resolved.

**HBitLogs** is a simple offline CLI habit tracker built with Python and SQLite3.  
Track your daily habits from the terminal — no network, no fluff.

## 🔧 Features

- Add new habits
- Log habits for the current day
- View habit statistics
- List all tracked habits
- Remove habits (with their logs)
- All data stored locally in SQLite

## 💻 Requirements

- Python 3.x

## 📦 Installation

```bash
git clone https://github.com/samm8g/hbitlogs.git
cd hbitlogs
```

(Optional: Create a virtual environment)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 🚀 Usage

```bash
# Add a habit
python hbitlogs.py add "Read book"

# Log it for today
python hbitlogs.py log "Read book"

# List all habits
python hbitlogs.py list

# Show stats for a habit
python hbitlogs.py stats "Read book"

# Remove a habit
python hbitlogs.py remove "Read book"
```

## 🗃️ Data

All data is stored locally in `hbitlogs.db`.  
You can inspect it manually using any SQLite viewer or CLI.

## 📚 Learning Goals

This project helped me learn and practice:

- Python 3 CLI development
- SQLite3 database integration
- Argparse for command-line parsing
- Organizing a minimal Python project

## 🛠️ TODO

- [ ] Track streaks
- [ ] Export to JSON/CSV
- [ ] Text-based calendar view
- [ ] TUI version (maybe with `rich` or `urwid`)

## 📄 License

MIT License — do whatever you want but don't sue me :)

---

Made with ☕ by [Samm8g](https://github.com/samm8g)
