# QuietQuill

A special highly secire diary app


QuietQuill/

    ├── main.py                  # App entry point
    ├── db/   
    │   └── users.db             # SQLite DB for user auth 
    ├── ui/
    │   ├── login_window.py             # Login screen
    │   ├── register_window.py          # Registration screen
    |   ├── advance_search.py    # Search funtion for files 
    |   ├── change_password.py   # Password change feature
    |   ├── entry_clandar.py     # Calandar display for entries
    |   ├── mood_tracker.py      # Mood tracking macanism
    |   ├── start.py             # 
    |   ├── editor.py            # word editor page 
    │   └── dashboard.py         # Diary dashboard after login
    ├── utils/
    │   └── encryption.py        # AES encryption/decryption
    ├── entries/                 # Encrypted entries per user
    ├── assets/                  # Icons/images
    ├── .gitignore               # git bash ignore files 
    ├── requirements.txt         # Dependencies list
    └── README.md
