from __future__ import annotations
from dataclasses import dataclass
from uuid import uuid4
from typing import Optional

from domain_model.models import Journal, Entry
from .encryption_strategy import EncryptionStrategy
from .repository_factory import EntryRepository


@dataclass
class JournalController:
    """GRASP Controller: Handles UI-initiated use cases for Journal.

    Collaborates with:
      - EntryRepository (Factory-produced)
      - EncryptionStrategy (GoF Strategy)
      - Domain objects retain Information Expert responsibilities (validate, etc.)
    """

    journal: Journal
    repo: EntryRepository
    crypto: EncryptionStrategy

    def create_entry(self, title: str, content: str, *, user: Optional[str] = None, encrypt: bool = False) -> Entry:
        e = Entry(entry_id=uuid4(), title=title, content=content)
        if encrypt:
            ciphertext = self.crypto.encrypt(e.content, user=user)
            e.content = ciphertext.decode("utf-8", errors="ignore")
            e.is_encrypted = True
        e.validate()
        self.journal.add_entry(e)
        self.repo.save(e)
        return e

    def export_all(self) -> int:
        items = self.repo.all()
        # For demo, return count; actual export would write a package/zip
        return len(items)
