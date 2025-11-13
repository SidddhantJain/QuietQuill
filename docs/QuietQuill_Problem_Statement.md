# QuietQuill — Problem Statement (SRS-aligned)

AIM: Identify a project of sufficient complexity (≥ 4–5 major functionalities) and write a detailed problem statement.

Title: QuietQuill — Privacy‑First, Offline‑First Personal Journaling System

## Introduction
Educational, clinical, and personal wellbeing contexts increasingly value reflective practice and mood tracking. Many journaling apps, however, are cloud‑centric and require continuous connectivity, introducing privacy risks and data lock‑in. QuietQuill addresses these concerns by providing a desktop journaling application that runs entirely on the user’s device, supports on‑device encryption, and remains fully functional offline while still offering fast search, analytics, and optional encrypted backups.

## Problem Statement
Current journaling workflows are fragmented: users switch between editors, file systems, and ad‑hoc backup habits. Cloud‑dependent tools expose sensitive content to third parties and require network availability. Users need a unified, private, and dependable journaling experience that:
- Works offline without compromising features.
- Keeps content under the user’s control (local‑first storage, on‑device encryption).
- Provides fast search, mood/stats insights, and calendar views.
- Offers optional, user‑controlled backup/export without leaking plaintext.

Hence, we propose an object‑oriented, modular system that integrates secure authoring, indexing, analysis, and backup with clear separation of concerns.

## Major Functionalities (core 5)
1. Secure Authentication and Session Management
   - Local user profile; credentials/salts managed in a local SQLite DB.
   - Optional remember‑me tokens stored securely.
2. Rich Entry Authoring and Management
   - Editor with autosave, unsaved‑changes prompt, tags, categories, attachments (images/files).
   - Per‑entry encryption toggle; metadata preserved.
3. Advanced Search and Filtering
   - Inverted index for fast text search; filters by date, tags, category.
   - Advanced search UI with saved queries.
4. Mood and Stats Analytics
   - Lightweight text analysis for mood signals; per‑period stats (counts, tags, attachments).
   - Dashboards and visual summaries.
5. Export/Backup and Restore
   - Local exports (JSON/ZIP); optional encrypted cloud backup via HTTPS/TLS.
   - Restore flow with verification; on‑device decryption.

(Additional extensible features: calendar/timeline view, profile‑based security policies, multi‑journal support.)

## Scope of the Project
- Platform: Windows desktop (packaged via PyInstaller as `QuietQuill.exe`).
- Storage: Local filesystem for entries/media; local SQLite for credentials/salts.
- Network: Optional only—used for encrypted backup; app remains fully usable offline.
- Architecture: Layered (Presentation, Application/Controllers, Domain, Infrastructure). Interfaces enable Strategy/Factory/Observer patterns for swappable encryption, repositories, and event‑driven features (autosave/index/mood).

## 6W: Who / What / Where / When / Why / How
- Who is the application for?
  - Individuals who value privacy and offline reliability (students, professionals, therapists’ clients). Secondary: advisors who recommend private journaling tools.
- What problem will it solve?
  - Eliminates reliance on cloud and scattered tools; provides a single, private, fully‑featured journaling workspace with fast search, insights, and safe backup/restore.
- Where will it be used?
  - On users’ own devices (desktop). Optional cloud storage is used only for encrypted backups.
- When is it needed?
  - Daily for capturing reflections; at save/export/backup times; during review/analysis; during recovery from device issues.
- Why is it needed?
  - To protect sensitive content while providing productivity and insights; to ensure availability without network; to keep ownership and transparency over data flows.
- How will it work?
  - UI delegates to controllers; controllers use domain services via interfaces (IEntryRepository, IEncryption, IAnalyzer). Entries are stored locally; encryption happens on device. Optional backups use secure channels and can be encrypted prior to upload.

## Non‑Functional Requirements (summary)
- Privacy/Security: On‑device encryption; no plaintext leaves device without explicit export; per‑user key derivation with salts.
- Performance: Launch ≤ 2s typical; search ≤ 200ms for 10k entries; autosave ≤ 100ms per change burst (debounced).
- Reliability: Autosave; recoverable exports/backups; minimal data loss windows.
- Usability/Accessibility: Distraction‑free UI; clear affordances and error messages.
- Portability: Windows packaging; future cross‑platform feasible.

## Constraints and Assumptions
- Single‑user desktop by default; no server required.
- Optional cloud storage is user‑configured and uses HTTPS/TLS; recommend client‑side encryption before upload.
- Python implementation packaged with PyInstaller; local dependencies bundled.

## Deliverables / Output
- This problem statement (SRS‑aligned) as Markdown; export to PDF for submission.
- UML artifacts (already in repo):
  - Use Case, Activity (swimlanes), Sequence, Class (with OCL), Profile, Component, State, Deployment diagrams in `uml/`.
- Runnable prototypes:
  - State machine demo: `state_model/demo.py`
  - Patterns demos (Strategy/Factory/Observer): `patterns/demo.py`, `patterns/observer_demo.py`

## Conclusion
QuietQuill delivers a privacy‑first, offline‑first journaling experience by consolidating authoring, search, analytics, and backup into a cohesive, local‑first design. Its modular, interface‑driven architecture supports strong security boundaries and future extensibility (e.g., sync, new storage strategies) without sacrificing user control or performance.

## References
- Blaha, M., & Rumbaugh, J. (2005). Object‑Oriented Modeling and Design with UML (Chapter 3: Class Modeling).
- Organization or course LMS requirement specification (as a template reference for SRS structure).
- Project UML artifacts in this repository’s `uml/` folder (PlantUML/XMI/Mermaid).

---

### PDF Export (quick)
- In VS Code: Open this file → Right‑click → “Open Preview” → Print to PDF (or use the Markdown PDF extension if installed).
- Alternative: Copy into a word processor (Word/Google Docs) and export to PDF.
