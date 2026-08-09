import os

basedir = os.path.abspath(os.path.dirname(__file__))


def get_database_uri():
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return database_url

    if os.environ.get('VERCEL'):
        db_dir = '/tmp'
    else:
        db_dir = basedir

    os.makedirs(db_dir, exist_ok=True)
    return 'sqlite:///' + os.path.join(db_dir, 'trek_manager.db')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'trekking-secret-key')
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
