import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")
    SECRET_KEY = os.environ.get("SECRET_KEY") or "asjdbhGHBFASn"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(BASE_DIR, 'post_database.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    template_dir = os.path.join(BASE_DIR, "templates")
