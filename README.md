
# Learning Scheduler 🧠📚

A web app built with Flask to help students stay productive by managing subjects, tracking progress, following Pomodoro sessions, and organizing timetables...

---

 🚀 Features

- 🧾 User Registration & Login
- 📊 Dashboard with study progress tracking
- ⏱️ Pomodoro Timer for focused study
- 📘 Add & Manage Subjects
- 📅 Timetable view
- 🗂️ Organized templates and static assets

---

## 🛠️ Tech Stack

- Backend: Python (Flask)
- Frontend: HTML, CSS(Bootstrap), JavaScript,jinja2
- Database: SQLite
- Others: Flask-WTF (Forms), Scheduler

---

## 📂 Project Structure

```
project/
│
├── app.py                # Main Flask app
├── forms.py              # Flask-WTF forms
├── scheduler.py          # Background task scheduler
├── requirements.txt      # Python dependencies
│
├── templates/            # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   ├── ...
│
├── static/               # Static files
│   ├── css/style.css
│   └── js/main.js
│
├── instance/
│   └── database.db       # SQLite database
│
└── venv/                 # Virtual environment (not needed to push on GitHub)
```

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask app:**
   ```bash
   python app.py
   ```

---

## 🤝 Collaborators

- **Nandan Garg** – Feature Integration ,database and Testing
- **Ayush Juyal** – Backend & Flask Integration
- **Avish Pradhan** –  UI/UX Design and Frontend Support


---

## 🔒 Note

Do not push `venv/` or `instance/database.db` to GitHub. Add them to your `.gitignore` file like this:

```bash
venv/
instance/
__pycache__/
```

---

## 📃 License

This project is open-source and available under the [MIT License](LICENSE).
