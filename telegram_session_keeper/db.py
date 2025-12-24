import csv
import fcntl
from datetime import datetime

from telegram_session_keeper.settings import settings

__all__ = ["HEADERS", "append_session", "remove_session", "get_sessions_list", "get_session"]

HEADERS = ["phone", "created", "session"]


def append_session(phone: str, session: str) -> bool:
    # Write headers
    if not settings.db_path.exists():
        with open(settings.db_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

    with open(settings.db_path, "r+", newline="", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)  # Lock file

        reader = csv.DictReader(f)
        rows = list(reader)

        for row in rows:
            if row["phone"] == phone:
                fcntl.flock(f, fcntl.LOCK_UN)

                return False

        f.seek(0, 2)

        writer = csv.writer(f)
        writer.writerow([phone, datetime.utcnow().isoformat(timespec="YYYY-MM-DD_HH-MM-SS"), session])

        fcntl.flock(f, fcntl.LOCK_UN)  # Release the lock

        return True


def remove_session(phone: str) -> bool:
    with open(settings.db_path, "r+", newline="", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)  # Lock file

        reader = csv.DictReader(f)

        old_rows = list(reader)
        new_rows = []

        for row in old_rows:
            if row["phone"] != phone:
                new_rows.append(row)

        fcntl.flock(f, fcntl.LOCK_UN)  # Release the lock

    if len(new_rows) == len(old_rows):
        return False

    with open(settings.db_path, "w+", newline="", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)  # Lock file

        writer = csv.writer(f)
        writer.writerow(HEADERS)
        writer.writerows(new_rows)

        fcntl.flock(f, fcntl.LOCK_UN)  # Release the lock

    return True


def get_sessions_list() -> list:
    with open(settings.db_path, "r", newline="", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)  # Lock file
        reader = csv.DictReader(f)
        fcntl.flock(f, fcntl.LOCK_UN)  # Release the lock

        return list(reader)


def get_session(phone: str) -> str | None:
    with open(settings.db_path, "r", newline="", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)  # Lock file

        reader = csv.DictReader(f)
        for row in reader:
            if row["phone"] == phone:
                return row["session"]

        fcntl.flock(f, fcntl.LOCK_UN)  # Release the lock
