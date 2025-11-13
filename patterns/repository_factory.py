from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from dataclasses import asdict
import json

from domain_model.models import Entry


class EntryRepository(ABC):
    """Abstract repo for Entries (Factory Method target)."""

    @abstractmethod
    def save(self, entry: Entry) -> None: ...

    @abstractmethod
    def all(self) -> List[Entry]: ...


class InMemoryEntryRepository(EntryRepository):
    def __init__(self) -> None:
        self._items: List[Entry] = []

    def save(self, entry: Entry) -> None:
        self._items.append(entry)

    def all(self) -> List[Entry]:
        return list(self._items)


class FileEntryRepository(EntryRepository):
    def __init__(self, folder: Path) -> None:
        self._folder = folder
        self._folder.mkdir(parents=True, exist_ok=True)

    def save(self, entry: Entry) -> None:
        p = self._folder / f"{entry.entry_id}.json"
        with p.open("w", encoding="utf-8") as f:
            json.dump(asdict(entry), f, default=str, ensure_ascii=False, indent=2)

    def all(self) -> List[Entry]:
        items: List[Entry] = []
        for p in self._folder.glob("*.json"):
            try:
                # For demo only; we don't reconstruct datetimes properly here
                data = json.loads(p.read_text(encoding="utf-8"))
                items.append(Entry(**data))
            except Exception:
                continue
        return items


class RepositoryFactory:
    """GoF Factory Method: choose concrete repository at runtime."""

    def create_entry_repo(self, kind: str = "memory", *, folder: str | None = None) -> EntryRepository:
        kind = (kind or "memory").lower()
        if kind == "file":
            if not folder:
                raise ValueError("folder required for file repository")
            return FileEntryRepository(Path(folder))
        return InMemoryEntryRepository()
