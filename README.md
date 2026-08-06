# Trekspire Trek Management System

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
