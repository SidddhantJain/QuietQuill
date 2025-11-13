# Deployment View (Concise)

Nodes
- User Device (Desktop Runtime, PyInstaller app)
- UsersDB (SQLite file)
- FileSystem (entries, exports/backups)
- Internet (HTTPS)
- Cloud Object Storage (optional backup bucket)

Strategy
- Privacy/offline‑first: all processing local; backups optional.
- Security: encrypt on device; HTTPS for remote.

Placement rationale
- Single executable: simple distribution, low latency.
- SQLite/file storage: no server required; portable.
- Optional cloud: durability without changing app internals.
