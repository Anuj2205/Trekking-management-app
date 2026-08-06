# Trekspire Trek Management System

## Setup

1. Install Python 3.11 or newer from https://www.python.org/downloads/windows.
2. During installation, enable "Add Python to PATH".
3. Open PowerShell and run:

```powershell
cd "c:\Users\anujd\Desktop\iitm project"
python --version
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

If `python` still fails, try `python3`.

## Run

- Open `http://127.0.0.1:5000` in your browser.

## Project structure

- `app.py` - Flask entrypoint
- `config.py` - application configuration
- `app/models` - SQLAlchemy models
- `app/routes` - Flask blueprints
- `app/forms` - WTForms forms
- `app/templates` - Jinja2 templates
- `app/static/css` - custom styling

## Notes

- SQLite database is created automatically.
- Use the registration page to create a user account.
- Admin pages require a user with role `admin`.
