from __future__ import annotations

from uuid import uuid4
from pathlib import Path

from domain_model.models import new_user, Journal
from patterns.encryption_strategy import NoOpStrategy, ReversibleStrategy
from patterns.repository_factory import RepositoryFactory
from patterns.controller import JournalController


def run_demo() -> None:
    # Setup: user+journal, factory decides repository kind
    user = new_user("sid", "hash123")
    journal = Journal(id=uuid4(), owner=user)

    repo = RepositoryFactory().create_entry_repo("memory")

    # Choose encryption strategy at runtime (GoF Strategy)
    crypto = ReversibleStrategy()  # switch to NoOpStrategy() to see cleartext

    controller = JournalController(journal=journal, repo=repo, crypto=crypto)

    # Use cases via GRASP Controller
    e1 = controller.create_entry("Day 1", "Feeling happy and great today.")
    e2 = controller.create_entry("Day 2", "A bit sad, but hopeful.", encrypt=True)

    count = controller.export_all()

    print("Entry1: ", e1.title, e1.is_encrypted)
    print("Entry2: ", e2.title, e2.is_encrypted)
    print("Export count:", count)


if __name__ == "__main__":
    run_demo()
