# Component View (Concise)

- Presentation: LoginWindow, Dashboard, Editor, Search (thin UI; delegates to controllers)
- Application: AuthController, EntryController, RepositoryFactory
- Domain: IAuth, IEntryRepository, IEncryption (Strategy), IAnalyzer (Strategy)
- Infrastructure: AuthService (SQLite), InMemory/FileEntryRepository, ExportService, BackupService, FileSystem

Why this split
- SoC and testability (UIs thin; controllers orchestrate; adapters isolate IO)
- Substitutability (Strategy/Factory behind interfaces)
- Security boundary (Auth + encryption separated; cloud optional)

Dependencies
- UI → Controllers (use cases)
- Controllers → Interfaces (IAuth/IRepo/ICrypto/IAnalyzer)
- Adapters realize interfaces; Export/Backup handle IO outside controllers
