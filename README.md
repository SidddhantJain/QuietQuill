<div align="center">
  <img src="https://img.shields.io/badge/PyQt5-Desktop%20Application-blue" alt="PyQt5 Desktop Application" />
  <img src="https://img.shields.io/badge/Security-AES%20Encrypted-green" alt="AES Encrypted" />
  <img src="https://img.shields.io/badge/Python-3.8+-brightgreen" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License" />
  
  <h1>📝 QuietQuill ✨</h1>
  <p>
    <b>A secure, modern, and feature-rich digital diary application</b><br>
    <i>Built with Python & PyQt5 - Your thoughts, encrypted and protected</i>
  </p>
</div>

---

## 🚀 Overview

**QuietQuill** is a highly secure, modern diary application that prioritizes your privacy above everything else. With AES encryption, mood tracking, calendar views, and a beautiful responsive interface, QuietQuill transforms the way you journal. Every entry is encrypted before being saved to disk, ensuring your most personal thoughts remain truly private.

---

## ✨ Features

- 🔐 **Military-Grade Security:** AES encryption for all diary entries
- 🎨 **Beautiful Modern UI:** Card-based design with gradients and shadows
- 🌙 **Dark & Light Themes:** Switch between elegant themes
- 📝 **Rich Text Editor:** Format text, insert images, emojis, and more
- 📅 **Mood Tracker:** Track daily emotions with interactive calendar
- 📊 **Writing Statistics:** Insights into your writing habits and patterns
- 🏷️ **Smart Tagging:** Organize entries with categories and tags
- 🔍 **Advanced Search:** Find entries by tags, title, date, or content
- 📆 **Calendar View:** Visualize your entries across time
- 💾 **Local Storage:** No cloud dependency - your data stays on your device
- 🔄 **Responsive Design:** Scales beautifully across different screen sizes

---

## 📱 Screenshots

*Coming soon - Beautiful UI screenshots showcasing the modern interface*

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start (Windows PowerShell)

1. Clone the repository
   ```powershell
   git clone https://github.com/yourusername/QuietQuill.git
   cd QuietQuill
   ```

2. Create and activate a virtual environment
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   ```

3. Install dependencies
   ```powershell
   pip install -r requirement.txt
   ```

4. Initialize the database (creates db/users.db if missing)
   ```powershell
   python -c "from db.init_db import init_db; init_db()"
   ```

5. Run the app from source
   ```powershell
   python .\main.py
   ```

6. Optional: run the packaged executable (if present)
   ```powershell
   .\build\main\QuietQuill.exe
   ```

---

## 📂 Project Architecture

```
QuietQuill/
├── 📄 main.py                  # Application entry point
├── 🗄️ db/
│   ├── init_db.py             # Database initialization
│   └── users.db               # SQLite user database
├── 🎨 ui/
│   ├── login_window.py        # Secure login interface
│   ├── register_window.py     # User registration
│   ├── dashboard.py           # Main application hub
│   ├── editor.py              # Rich text editor
│   ├── mood_tracker.py        # Emotional tracking
│   ├── entry_calendar.py      # Calendar visualization
│   ├── stats.py               # Writing analytics
│   └── change_password.py     # Password management
├── 🔒 utils/
│   └── encryption.py          # AES encryption utilities
├── 📁 entries/                # Encrypted user entries
├── 📋 requirements.txt        # Python dependencies
└── 📖 README.md               # This file
```

---

## 🖼️ UML Diagrams (Class Model + OCL)

- Class diagram source: `uml/Class_Model_QuietQuill.puml`
- OCL specification: `uml/OCL_QuietQuill.md`

How to preview/export the class diagram:
- VS Code: install the PlantUML extension, open the `.puml` file, then “Preview Current Diagram” and Export as PNG/SVG.
- Alternatively (CLI): use PlantUML + Graphviz locally to render the `.puml` to images.

---

## 🔒 Security Features

- **🛡️ AES Encryption:** All diary entries encrypted before storage
- **🧂 Salted Passwords:** Secure password hashing with random salts
- **🏠 Local Storage:** No cloud uploads - complete data sovereignty
- **🔐 Session Management:** Secure login/logout mechanisms
- **💾 File Integrity:** Metadata protection and validation

---

## 🎯 Getting Started

### First Time Setup
1. Launch the application
2. Click "Register" to create your account
3. Choose a strong password (your encryption key!)
4. Start writing your first entry

### Daily Usage
- **Dashboard:** View all entries, search, and navigate
- **New Entry:** Click "➕ New Entry" to start writing
- **Mood Tracking:** Record daily emotions in the mood tracker
- **Statistics:** Check your writing patterns and progress

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/QuietQuill.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

---

## 📋 Requirements

```
PyQt5>=5.15.0
cryptography>=3.4.8
sqlite3
hashlib
binascii
datetime
json
os
```

---

## 🐛 Known Issues & Roadmap

### Current Limitations
- Single user per installation
- Desktop only (no mobile app yet)

### Future Enhancements
- [ ] Multi-user support
- [ ] Export/Import functionality
- [ ] Plugin system
- [ ] Mobile companion app
- [ ] Advanced text formatting
- [ ] Voice notes integration

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **PyQt5 Team** - For the amazing GUI framework
- **Python Community** - For the robust ecosystem
- **Security Researchers** - For encryption best practices
- **Open Source Contributors** - For inspiration and code quality standards

---

## 📞 Support & Contact

- 🐛 **Found a bug?** [Open an issue](https://github.com/yourusername/QuietQuill/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/yourusername/QuietQuill/discussions)
- 📧 **Email:** your.email@example.com
- 🐦 **Twitter:** [@yourusername](https://twitter.com/yourusername)

---

<div align="center">
  <h3>🌟 If QuietQuill helps you, please consider giving it a star! 🌟</h3>
  <p><b>Made with ❤️ and ☕ by Siddhant Jain</b></p>
  <p><i>"Your thoughts deserve privacy, your memories deserve protection."</i></p>
</div>

---
