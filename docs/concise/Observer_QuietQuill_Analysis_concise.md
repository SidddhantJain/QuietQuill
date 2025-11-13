# Observer Pattern (Concise)

Problem
- On typing/saving, multiple reactions needed: autosave, re‑index, mood update, UI status.

Solution (Observer)
- Subject: EntrySubject publishes CONTENT_CHANGED, SAVED, SYNC_DONE.
- Observers: AutoSave, Index, Mood, UIStatus (independent, pluggable).

Implementation
- Autosave: save on CONTENT_CHANGED (no content mutation); encrypt on SAVED if requested.
- Index: update inverted index on CONTENT_CHANGED.
- Mood: recompute mood score on CONTENT_CHANGED.
- UI: set status (typing/saved/synced).

Result
- Loose coupling, open‑closed, testable observers; easy to add/remove behaviors.
