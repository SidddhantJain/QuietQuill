from __future__ import annotations
from uuid import uuid4

from domain_model.models import Journal, new_user, new_entry
from patterns.repository_factory import InMemoryEntryRepository
from patterns.encryption_strategy import ReversibleStrategy
from patterns.observer import (
    EntrySubject,
    AutoSaveObserver,
    IndexObserver,
    MoodObserver,
    UIStatusObserver,
    EventType,
)


def run_demo() -> None:
    user = new_user("sid", "hash123")
    journal = Journal(id=uuid4(), owner=user)

    subj = EntrySubject()

    autosave = AutoSaveObserver(repo=InMemoryEntryRepository(), crypto=ReversibleStrategy())
    indexer = IndexObserver()
    mood = MoodObserver()
    ui = UIStatusObserver()

    subj.attach(autosave)
    subj.attach(indexer)
    subj.attach(mood)
    subj.attach(ui)

    # Create an entry and simulate typing (content changed)
    e = new_entry("Day 1", "Feeling happy and great today.")
    journal.add_entry(e)

    # Notify observers of content change
    subj.notify(EventType.CONTENT_CHANGED, {"entry": e, "user": user.username, "encrypt": True})

    # Simulate a save event
    subj.notify(EventType.SAVED, {"entry": e, "user": user.username, "encrypt": True})

    # Check resulting states
    print("UI status:", ui.last_message)
    print("Mood score:", mood.last_score)
    # Basic search: ensure some token is indexed
    token = "happy"
    in_index = e.entry_id in indexer.index.get(token, set())
    print(f"Indexed '{token}':", in_index)


if __name__ == "__main__":
    run_demo()
