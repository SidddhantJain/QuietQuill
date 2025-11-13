from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict, List, Set, DefaultDict
from collections import defaultdict
from uuid import UUID

from domain_model.models import Entry
from domain_model.services import MoodAnalyzer
from .repository_factory import EntryRepository, InMemoryEntryRepository
from .encryption_strategy import EncryptionStrategy, NoOpStrategy, ReversibleStrategy


class EventType(Enum):
    CONTENT_CHANGED = auto()
    SAVED = auto()
    SYNC_DONE = auto()


class Observer(ABC):
    @abstractmethod
    def update(self, subj: "Subject", evt: EventType, data: Dict[str, Any]) -> None:
        ...


class Subject(ABC):
    @abstractmethod
    def attach(self, o: Observer) -> None: ...

    @abstractmethod
    def detach(self, o: Observer) -> None: ...

    @abstractmethod
    def notify(self, evt: EventType, data: Dict[str, Any]) -> None: ...


class EntrySubject(Subject):
    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, o: Observer) -> None:
        if o not in self._observers:
            self._observers.append(o)

    def detach(self, o: Observer) -> None:
        if o in self._observers:
            self._observers.remove(o)

    def notify(self, evt: EventType, data: Dict[str, Any]) -> None:
        for o in list(self._observers):
            o.update(self, evt, data)


class AutoSaveObserver(Observer):
    """Autosaves entry on content change (debounced externally) and on explicit save events."""

    def __init__(self, repo: EntryRepository | None = None, crypto: EncryptionStrategy | None = None) -> None:
        self._repo = repo or InMemoryEntryRepository()
        self._crypto = crypto or NoOpStrategy()

    def update(self, subj: Subject, evt: EventType, data: Dict[str, Any]) -> None:
        entry: Entry = data["entry"]
        if evt == EventType.CONTENT_CHANGED:
            # Save plaintext snapshot as user types (no mutation of entry content)
            self._repo.save(entry)
        elif evt == EventType.SAVED:
            # On explicit save, optionally encrypt before persisting
            encrypt = data.get("encrypt", False)
            if encrypt and not isinstance(self._crypto, NoOpStrategy):
                ct = self._crypto.encrypt(entry.content, user=data.get("user"))
                entry.content = ct.decode("utf-8", errors="ignore")
                entry.is_encrypted = True
            self._repo.save(entry)


class IndexObserver(Observer):
    """Maintains a simple inverted index for search suggestions."""

    def __init__(self) -> None:
        self.index: DefaultDict[str, Set[UUID]] = defaultdict(set)

    def update(self, subj: Subject, evt: EventType, data: Dict[str, Any]) -> None:
        if evt == EventType.CONTENT_CHANGED:
            entry: Entry = data["entry"]
            words = {w.strip(".,!?:;()[]{}\"'\n\t\r").lower() for w in entry.content.split() if w}
            for w in words:
                if w:
                    self.index[w].add(entry.entry_id)


class MoodObserver(Observer):
    """Recomputes mood metrics when content changes."""

    def __init__(self) -> None:
        self._an = MoodAnalyzer()
        self.last_score: int | None = None

    def update(self, subj: Subject, evt: EventType, data: Dict[str, Any]) -> None:
        if evt == EventType.CONTENT_CHANGED:
            entry: Entry = data["entry"]
            res = self._an.analyze([entry])
            self.last_score = int(res.get("moodScore", 0))


class UIStatusObserver(Observer):
    """Updates UI status indicators (simulated by prints for this demo)."""

    def __init__(self) -> None:
        self.last_message: str | None = None

    def update(self, subj: Subject, evt: EventType, data: Dict[str, Any]) -> None:
        if evt == EventType.CONTENT_CHANGED:
            self.last_message = "typing…"
        elif evt == EventType.SAVED:
            self.last_message = "saved"
        elif evt == EventType.SYNC_DONE:
            self.last_message = "synced"


__all__ = [
    "EventType",
    "Observer",
    "Subject",
    "EntrySubject",
    "AutoSaveObserver",
    "IndexObserver",
    "MoodObserver",
    "UIStatusObserver",
]
