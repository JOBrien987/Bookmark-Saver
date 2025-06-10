# Bookmark-Saver
# Bookmark Saver

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)

  * [Option A: Python Script](#option-a-python-script)
  * [Option B: Windows Installer](#option-b-windows-installer)
* [Usage](#usage)
* [Configuration](#configuration)
* [Scheduled Backups](#scheduled-backups)
* [Uninstallation](#uninstallation)
* [Troubleshooting](#troubleshooting)
* [Contributing](#contributing)
* [License](#license)
* [Author](#author)

---

## Overview

**Bookmark Saver** is a simple utility that automatically backs up your Firefox bookmarks daily. It:

1. Locates your default Firefox profile across Windows, macOS, and Linux.
2. Copies the `places.sqlite` database to a timestamped backup directory.
3. Exports all bookmarks into a human-readable HTML file.
4. Can be run directly as a Python script or installed as a Windows application with a native installer.

Use this tool to ensure you never lose your bookmarks—even if your profile gets corrupted.

---

## Features

* Cross-platform profile detection (Windows, macOS, Linux)
* Atomic backup of Firefox’s `places.sqlite`
* HTML export of all bookmarks (organized alphabetically)
* Daily automated scheduling via the built‑in scheduler
* Optionally packaged as a one‑file Windows executable

---

## Requirements

* Python 3.7 or higher
* [schedule](https://pypi.org/project/schedule/) Python package (for script scheduling)
* (For Windows installer) [PyInstaller](https://www.pyinstaller.org/) and [Inno Setup](https://jrsoftware.org/) to build

---

## Installation

### Option A: Python Script

1. **Clone this repo**

   ```bash
   git clone https://github.com/yourusername/bookmark-saver.git
   cd bookmark-saver
   ```

2. **Install dependencies**

   ```bash
   pip install schedule
   ```

3. **Run the script**

   ```bash
   python bookmark_saver.py
   ```

This will perform an immediate backup and then continue running, triggering a backup daily at 02:00 by default.

### Option B: Windows Installer

Built using PyInstaller and Inno Setup.

1. **Build the EXE**

   ```powershell
   pyinstaller --onefile --name bookmark_saver bookmark_saver.py
   ```

   The output will appear in `dist\bookmark_saver.exe`.

2. **Compile the installer**

   * Open `bookmark_saver_installer.iss` in Inno Setup.
   * Click **Compile** (F9).
   * The installer `BookmarkSaverInstaller.exe` will appear in the `Output\` folder.

3. **Run the installer**
   Double-click `BookmarkSaverInstaller.exe` and follow the prompts.

---

## Usage

After installation or script launch, backups are written under:

```text
~/firefox_bookmark_backups/
  places_YYYYMMDD_HHMMSS.sqlite
  bookmarks_YYYYMMDD_HHMMSS.html
```

Open the `.html` file in any browser to view your saved bookmarks.

---

## Configuration

* **Backup time**: Set the `FIREFOX_BACKUP_TIME` environment variable to change the daily backup time (format: `HH:MM`, 24‑hour).

* **Backup directory**: By default, backups go to `~/firefox_bookmark_backups`. To change this, edit the `backup_dir` path in the script.

---

## Scheduled Backups

The Python script uses the `schedule` library to trigger backups daily at the configured time. To run it automatically on system startup:

* **Windows**: Add a shortcut to `bookmark_saver.exe` in your Startup folder.
* **Linux/macOS**: Create a cron job, e.g.:

  ```cron
  @reboot /usr/bin/env python3 /path/to/bookmark_saver.py
  ```

---

## Uninstallation

* **Script**: simply delete the script and backup folder.
* **Installer**: use **Add/Remove Programs** on Windows to uninstall "Bookmark Saver".

---

## Troubleshooting

* **`profiles.ini not found`**: Ensure Firefox has been run at least once and you have a default profile.
* **Permission errors**: On Linux/macOS, you may need `chmod +x bookmark_saver.py` or run with `sudo` if backing up system‑protected folders.
* **Scheduler not running**: Verify the script/process is active; check logs or console output for errors.

---

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add feature XYZ"`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

Please follow the [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/) and include tests where applicable.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Author

**Jeremiah O'Brien** ([jayobrien987@gmail.com](mailto:jayobrien987@gmail.com))

Feedback and suggestions welcome!")
