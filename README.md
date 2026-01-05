# Minimal Resume Builder

A fast, clean, and professional Resume Builder built with Flask and Vanilla JS.
Designed for simplicity and performance.

## Features

- **Real-time Preview**: See your resume update as you type.
- **ATS-Friendly PDF**: Generates clean, text-based PDFs using ReportLab.
- **Minimal UI**: Distraction-free interface with 5 background styles.
- **Local Database**: SQLite support (optional for future extension).

## Setup

1.  **Clone the repository** (or download files).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application**:
    ```bash
    python app.py
    ```
4.  **Open in Browser**:
    Go to `http://localhost:5000`

## Deployment

This project is ready for deployment on platforms like Render, Railway, or Heroku.

- **Procfile** included for Gunicorn.
- **requirements.txt** up to date.
- **Environment**: Python 3.10+ recommended.

## Tech Stack

- **Backend**: Python (Flask), ReportLab (PDF Generation), SQLAlchemy.
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla).
- **Database**: SQLite.
