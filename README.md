# ChronoList – Task & Time Tracker

A sleek, real-time todo list and time tracker featuring continuous timers and easy packaging into a standalone executable.

A Windows-only standalone GUI application for tracking time against tasks.

## Requirements

- Python 3.9+ (tested on Windows)
- Packages:

  pip install -r requirements.txt

## Running the App

### In development

1. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:

   ```bash
   python src/main.py
   ```

The app stores its database file (`todo_tracker.db`) in your home directory.

## Packaging as Executable

To build a standalone Windows `.exe`:

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Run PyInstaller (from your project root):

   ```bash
  pyinstaller \
    --onefile               \  # single executable
    --windowed              \  # no console window
    --name chronolist       \  # executable name
    --icon assets/logo.ico  \  # path to your .ico file
    src/main.py
   ```

3. Find the executable in the `dist/` folder (e.g. `chronolist.exe`). Copy this to any Windows machine.

## Branding Assets

Place your custom application icons in the `assets/` directory:
- `assets/logo.png` – used for the window icon during runtime
- `assets/logo.ico` – used for the packaged executable

## MVP Features

- Add, edit, delete tasks
- Start/stop timer for a selected task
- View accumulated time per task
- Persists data in SQLite database

## Project Structure

```
chronolist/
├── assets/          # place logo.png and logo.ico here
├── requirements.txt
├── README.md
└── src/
    ├── main.py
    ├── models.py
    ├── views.py
    └── controllers.py
```  