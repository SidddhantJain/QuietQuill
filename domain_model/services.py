from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict

from .models import Entry


class Analyzer(ABC):
    @abstractmethod
    def analyze(self, entries: List[Entry]) -> Dict:
        """Analyze a set of entries and return metrics."""
        raise NotImplementedError


class MoodAnalyzer(Analyzer):
    def analyze(self, entries: List[Entry]) -> Dict:
        # Placeholder: compute a dummy mood score
        score = 0
        for e in entries:
            text = e.content.lower()
            if any(word in text for word in ("happy", "joy", "great")):
                score += 1
            if any(word in text for word in ("sad", "bad", "angry")):
                score -= 1
        return {"moodScore": score, "count": len(entries)}


class StatsService(Analyzer):
    def analyze(self, entries: List[Entry]) -> Dict:
        return {
            "count": len(entries),
            "encrypted": sum(1 for e in entries if e.is_encrypted),
            "attachments": sum(len(e.attachments) for e in entries),
            "tags": sum(len(e.tags) for e in entries),
        }


class EncryptionService:
    def encrypt(self, text: str) -> str:
        # Simple reversible placeholder (do NOT use in production)
        return text[::-1]

    def decrypt(self, text: str) -> str:
        return text[::-1]


class FileRepository:
    def save(self, entry: Entry) -> None:
        # Stub: integrate with actual persistence layer if needed
        pass

    def backup(self) -> None:
        pass

    def export(self) -> None:
        pass


class AuthService:
    def login(self, username: str, pwd: str) -> bool:
        # Stub: assume success for demonstration
        return bool(username and pwd)
