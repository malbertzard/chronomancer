from croniter import croniter
from datetime import datetime
from typing import List
from core.models import CronEntry

def parse_crontab_text(text: str, start_time: datetime, end_time: datetime) -> List[CronEntry]:
    entries = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) < 6:
            continue

        schedule = " ".join(parts[:5])
        command = " ".join(parts[5:])

        entry = CronEntry(schedule=schedule, command=command, source="user-crontab")
        try:
            iter = croniter(schedule, start_time)
            next_time = iter.get_next(datetime)

            while next_time <= end_time:
                entry.occurrences.append(next_time)
                next_time = iter.get_next(datetime)

            if entry.occurrences:
                entries.append(entry)

        except Exception as e:
            print(f"Error parsing line: {line} ({e})")

    return entries
