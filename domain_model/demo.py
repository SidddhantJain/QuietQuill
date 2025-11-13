from datetime import date
from uuid import uuid4

from .models import new_user, new_entry, Journal, Tag
from .services import MoodAnalyzer, StatsService, EncryptionService


def main() -> None:
    user = new_user("alice", "hashed:123")
    journal = Journal(id=uuid4(), owner=user)

    e1 = new_entry("First", "I feel very happy today")
    e1.add_tag(Tag("personal"))

    e2 = new_entry("Second", "It was a bad day but I learned a lot")
    e2.add_tag(Tag("reflection"))

    journal.add_entry(e1)
    journal.add_entry(e2)

    print("Entries today:", len(journal.entries_by_date(date.today())))

    mood = MoodAnalyzer().analyze(journal.entries)
    stats = StatsService().analyze(journal.entries)
    print("Mood:", mood)
    print("Stats:", stats)

    crypto = EncryptionService()
    enc = crypto.encrypt("secret")
    dec = crypto.decrypt(enc)
    print("Crypto roundtrip:", enc, "->", dec)


if __name__ == "__main__":
    main()
