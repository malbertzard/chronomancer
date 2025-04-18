from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import json

@dataclass
class CronEntry:
    schedule: str
    command: str
    source: str = "unknown"
    occurrences: List[datetime] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "schedule": self.schedule,
            "command": self.command,
            "source": self.source,
            "occurrences": [dt.isoformat() for dt in self.occurrences]
        }

    def to_json(self, pretty: bool = False) -> str:
        if pretty:
            return json.dumps(self.to_dict(), indent=2)
        return json.dumps(self.to_dict())

    def to_text(self) -> str:
        lines = [f"{dt.isoformat()} -> {self.command}" for dt in self.occurrences]
        return "\n".join(lines)

@dataclass
class CronEntryList:
    entries: List[CronEntry]

    def to_json(self, pretty: bool = False) -> str:
        return json.dumps([entry.to_dict() for entry in self.entries], indent=2 if pretty else None)

    def to_text(self) -> str:
        return "\n\n".join(entry.to_text() for entry in self.entries)
