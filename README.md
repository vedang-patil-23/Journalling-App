# Journaling App (Summer 2023)

> **Note:** This project was developed in summer 2023 as a personal journaling application to help track daily thoughts and reflections. It's being uploaded to GitHub at a later date.

A simple and elegant personal journaling application to help you capture your thoughts, feelings, and daily experiences. Built with Flask and designed with a clean, intuitive interface, this app makes journaling a seamless part of your daily routine.

## ✨ Features

- **📝 Rich Journal Entries**: Write and format your thoughts with a clean, distraction-free editor
- **😊 Mood Tracking**: Tag entries with your current mood (Happy, Sad, Neutral, Excited, Anxious)
- **🏷️ Tag System**: Organize entries with custom tags for easy filtering
- **🔍 Smart Search**: Quickly find past entries by date, mood, tags, or keywords
- **🔒 Secure & Private**: User authentication ensures your journal remains personal
- **📱 Responsive Design**: Works beautifully on both desktop and mobile devices
- **📊 Entry Statistics**: Visualize your journaling habits over time

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd journaling
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   python init_db.py
   ```
   Default users created:
   - Admin: `admin` / `admin123` (Full access)
   - Viewer: `viewer` / `view123` (Read-only access)

6. **Run the application**
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000`

## 🛠 Deployment

### Local Production Setup
1. Update `.env` with production settings:
   - Set `FLASK_ENV=production`
   - Update `SECRET_KEY` with a strong secret
   - Configure a production database (SQLite is used by default for development)

2. Run with Gunicorn for better performance:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Cloud Deployment (e.g., Heroku, PythonAnywhere)
1. Create a `Procfile` with:
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
   ```
2. Set environment variables as shown in `.env.example`
3. Deploy following your platform's instructions

## 📝 Project Structure
```
journaling/
├── app.py             # Main application file
├── init_db.py         # Database initialization
├── requirements.txt   # Dependencies
├── static/            # Static files (CSS, JS, images)
└── templates/         # HTML templates
```

## 📅 About This Project
- **Created**: Summer 2023
- **Purpose**: Personal project to maintain a digital journal and learn web development
- **Tech Stack**: 
  - Backend: Python, Flask, SQLAlchemy
  - Frontend: HTML5, CSS3, JavaScript, Bootstrap 5
  - Database: SQLite (can be configured to use PostgreSQL/MySQL)

## 🔒 Security Notes
- Change default credentials before deploying to production
- Use environment variables for sensitive information
- Consider implementing HTTPS in production
- Regularly backup your journal database

## 📚 Related Projects
Check out my other summer 2023 projects:
- [Expense Tracker](https://github.com/vedang-patil-23/expense-tracker)
- [Habit Tracker](https://github.com/vedang-patil-23/habit-tracker)