# Bookmark Saver

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/) [![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A cross-platform Python tool that automatically backs up your Firefox bookmarks every day, exporting both the raw `places.sqlite` database and a human-readable HTML file.

---

## 🚀 Features

- **Daily Automated Backups** of Firefox `places.sqlite`  
- **HTML Export** of all bookmarks for easy browsing  
- **Configurable** backup time, directory, and retention policy via CLI flags or JSON config  
- **Rotating Logs** (file + console) for auditability  
- **Email Notifications** on success or failure (SMTP)  
- **Cloud Sync** to AWS S3  
- **Retention Policy**: auto-prune backups older than _N_ days  
- **Service/Daemon Support**  
  - Windows Task Scheduler  
  - Linux `systemd` unit & timer  
- **Minimal Tkinter GUI** for interactive settings  

---

## 🛠 Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/jobrien987/Bookmark-Saver.git
   cd Bookmark-Saver
   ```

2. **Install dependencies**  
   ```bash
   pip install schedule boto3
   ```
   > Tkinter comes bundled with most Python installs.

---

## ⚙️ Configuration

On first run the tool will generate a default config file at:

- **Windows:** `%APPDATA%\bookmark_saver\config.json`  
- **macOS/Linux:** `~/.bookmark_saver/config.json`

### Using the GUI
```bash
python bookmark_saver.py --gui
```
Fill in:
- **Backup Time** (HH:MM, 24-hour)
- **Backup Directory** (absolute path)
- **Retention (days)**

### Manual Edit
Open `config.json` in your editor and adjust:
```jsonc
{
  "backup_time": "02:00",
  "backup_dir": "C:\Users\You\BookmarkBackups",
  "retention_days": 30,
  "logging": {
    "log_file": "C:\Users\You\AppData\Roaming\bookmark_saver\bookmark_saver.log",
    "level": "INFO"
  },
  "email": {
    "smtp_server": "smtp.example.com",
    "smtp_port": 587,
    "username": "you@example.com",
    "password": "yourpassword",
    "to_addr": "notify@example.com"
  },
  "s3": {
    "aws_access_key": "AKIA…",
    "aws_secret_key": "…",
    "bucket": "my-firefox-backups"
  }
}
```

---

## ▶️ Usage

### One-time Backup
```bash
python bookmark_saver.py --once
```

### Continuous Daemon
```bash
python bookmark_saver.py
```
• Performs an immediate backup, then schedules daily at your configured time.

---

## 🗓 Automate as a Service

### Windows Task Scheduler
Run PowerShell **as Administrator**:
```powershell
schtasks /create /sc daily /tn "Bookmark Saver" `
  /tr "C:\Path\To\python.exe C:\…\bookmark_saver.py --once" `
  /st 02:00
```

### Linux systemd
Place the files in `/etc/systemd/system/`:

**bookmark-saver.service**  
```ini
[Unit]
Description=Daily Firefox Bookmark Saver

[Service]
ExecStart=/usr/bin/python3 /opt/bookmark_saver/bookmark_saver.py --once
User=youruser
```

**bookmark-saver.timer**  
```ini
[Unit]
Description=Run Bookmark Saver daily at 02:00

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable & start:
```bash
sudo systemctl enable --now bookmark-saver.timer
```

---

## 📂 Output & Logs

- **Backups:**  
  Folder structure under `backup_dir`:
  ```
  YYYY-MM-DDTHH-MM-SS/
    ├── places.sqlite
    └── bookmarks.html
  ```
- **Log File:**  
  - Windows: `%APPDATA%\bookmark_saver\bookmark_saver.log`  
  - macOS/Linux: `~/.bookmark_saver/bookmark_saver.log`

---

## 🛠 Troubleshooting

- **Profile not found?**  
  Ensure Firefox is installed and you have a `*.default` or `*.default-release` folder under your profiles directory:
  - Windows: `%APPDATA%\Mozilla\Firefox\Profiles`  
  - macOS/Linux: `~/.mozilla/firefox`
- **Database locked?**  
  Close Firefox (or make sure no other process is using `places.sqlite`) before running.

---

## 🤝 Contributing

1. Fork the repo  
2. Create a feature branch (`git checkout -b feature/awesome`)  
3. Commit your changes (`git commit -m "Add awesome feature"`)  
4. Push to your branch (`git push origin feature/awesome`)  
5. Open a Pull Request  

Please follow the existing code style and add tests where possible.

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
