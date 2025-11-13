# QuietQuill — Problem Statement (Concise)

AIM: Build a privacy‑first, offline‑first personal journaling app with 5+ core features.

Title: QuietQuill — Desktop Journaling (Local‑First, Encrypted)

## Problem (short)
- Cloud‑centric tools risk privacy and require network; manual workflows are fragmented.
- Users want one private place to write, search, analyze, and back up entries.
- Need: local‑first app with encryption, fast search, insights, and optional backups.

## Core functionalities
- Auth/session: local profile, hashed credentials in SQLite.
- Entry authoring: editor, autosave, tags/categories, attachments, per‑entry encryption.
- Search/filter: local inverted index; filter by date/tags/category.
- Mood/stats: simple text signals; counts/tags/attachments dashboards.
- Export/backup/restore: JSON/ZIP; optional encrypted cloud backup; restore flow.

## Scope
- Windows desktop (PyInstaller). Local files + SQLite. Works fully offline. Optional HTTPS backup.

## 6W
- Who: privacy‑minded individuals; secondary advisors/therapists.
- What: single private workspace with write/search/insights/backup.
- Where: user’s device; optional encrypted cloud backup.
- When: daily journaling; save/export/restore moments.
- Why: protect sensitive content; be productive offline; keep ownership.
- How: layered architecture (UI → controllers → domain via interfaces). Local storage; on‑device encryption.

## NFRs
- Privacy/security: on‑device encryption; no plaintext leaves device by default.
- Performance: fast launch/search/autosave on 10k entries.
- Reliability: autosave + recoverable backups.
- Usability: simple UI; clear feedback.

## Deliverables
- Problem statement, UML (use case/activity/sequence/class/profile/component/state/deployment), runnable demos.

## Conclusion (one‑liner)
Local‑first journaling with on‑device encryption and optional secure backups—fast, private, and extensible.
