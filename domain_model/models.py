from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Set, Optional
from uuid import uuid4, UUID


@dataclass(frozen=True)
class Tag:
    name: str


@dataclass(frozen=True)
class Category:
    name: str


@dataclass
class DiaryUser:
    user_id: UUID
    username: str
    password_hash: str


@dataclass
class Attachment:
    id: UUID
    filename: str
    size: int


@dataclass
class ImageAttachment(Attachment):
    width: int
    height: int


@dataclass
class FileAttachment(Attachment):
    mime_type: str


@dataclass
class Entry:
    entry_id: UUID
    title: str
    content: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_encrypted: bool = False
    tags: Set[Tag] = field(default_factory=set)
    category: Optional[Category] = None
    attachments: List[Attachment] = field(default_factory=list)

    def add_tag(self, tag: Tag) -> None:
        if tag in self.tags:
            raise ValueError("Tag already present (OCL: not self.tags->includes(t))")
        self.tags.add(tag)

    def attach(self, att: Attachment) -> None:
        self.attachments.append(att)

    def validate(self) -> None:
        if not self.title:
            raise ValueError("Entry.title must not be empty (OCL: self.title.size() > 0)")
        if self.is_encrypted and not self.content:
            raise ValueError(
                "Encrypted entries must have content (OCL: self.isEncrypted implies self.content->notEmpty())"
            )


@dataclass
class Journal:
    id: UUID
    owner: DiaryUser
    entries: List[Entry] = field(default_factory=list)

    def add_entry(self, e: Entry) -> None:
        e.validate()
        self.entries.append(e)

    def entries_by_date(self, d: date) -> List[Entry]:
        return [e for e in self.entries if e.created_at.date() == d]


# Convenience factories
def new_user(username: str, password_hash: str) -> DiaryUser:
    return DiaryUser(user_id=uuid4(), username=username, password_hash=password_hash)


def new_entry(title: str, content: str) -> Entry:
    return Entry(entry_id=uuid4(), title=title, content=content)
