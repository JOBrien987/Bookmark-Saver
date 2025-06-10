#!/usr/bin/env python3
"""
Firefox Bookmark Backup App
This script copies Firefox's places.sqlite file and exports bookmarks to HTML daily.
Requirements:
    pip install schedule
"""
import os
import shutil
import sqlite3
import time
import datetime
import schedule
import platform
from pathlib import Path


def find_firefox_profile():
    """Locate the default Firefox profile directory based on OS."""
    user_home = Path.home()
    system = platform.system()
    if system == "Windows":
        profiles_ini = user_home / "AppData" / "Roaming" / "Mozilla" / "Firefox" / "profiles.ini"
    elif system == "Darwin":
        profiles_ini = user_home / "Library" / "Application Support" / "Firefox" / "profiles.ini"
    else:  # Linux and others
        profiles_ini = user_home / ".mozilla" / "firefox" / "profiles.ini"
    if not profiles_ini.exists():
        raise FileNotFoundError(f"profiles.ini not found at {profiles_ini}")
    import configparser
    config = configparser.ConfigParser()
    config.read(profiles_ini)
    # First look for Default=1
    for section in config.sections():
        if config.has_option(section, "Default") and config.getint(section, "Default") == 1:
            path = config.get(section, "Path")
            is_rel = config.getboolean(section, "IsRelative", fallback=True)
            return profiles_ini.parent / path if is_rel else Path(path)
    # Fallback: first profile
    for section in config.sections():
        if config.has_option(section, "Path"):
            path = config.get(section, "Path")
            is_rel = config.getboolean(section, "IsRelative", fallback=True)
            return profiles_ini.parent / path if is_rel else Path(path)
    raise FileNotFoundError("No Firefox profile found in profiles.ini")


def backup_bookmarks():
    """Perform backup of places.sqlite and export bookmarks to HTML."""
    try:
        profile = find_firefox_profile()
    except Exception as e:
        print(f"Error locating Firefox profile: {e}")
        return
    src = profile / "places.sqlite"
    if not src.exists():
        print(f"Source file not found: {src}")
        return
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path.home() / "firefox_bookmark_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    # Copy SQLite file
    dest_sql = backup_dir / f"places_{timestamp}.sqlite"
    shutil.copy2(src, dest_sql)
    print(f"Backed up SQLite to {dest_sql}")
    # Export to HTML
    html_file = backup_dir / f"bookmarks_{timestamp}.html"
    try:
        conn = sqlite3.connect(src)
        cur = conn.cursor()
        cur.execute("""
            SELECT b.title, p.url
            FROM moz_bookmarks b
            JOIN moz_places p ON b.fk = p.id
            WHERE b.type = 1
            ORDER BY b.title;
        """)
        rows = cur.fetchall()
        with open(html_file, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n<html><head><meta charset='utf-8'><title>Firefox Bookmarks Backup</title></head><body>\n<ul>\n")
            for title, url in rows:
                if url:
                    label = title if title else url
                    f.write(f"  <li><a href=\"{url}\">{label}</a></li>\n")
            f.write("</ul>\n</body></html>")
        print(f"Exported HTML bookmarks to {html_file}")
    except Exception as e:
        print(f"Error exporting HTML: {e}")
    finally:
        conn.close()


def main():
    # Initial backup
    backup_bookmarks()
    # Schedule daily
    backup_time = os.getenv("FIREFOX_BACKUP_TIME", "02:00")
    schedule.every().day.at(backup_time).do(backup_bookmarks)
    print(f"Scheduled daily backups at {backup_time}")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
