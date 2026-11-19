import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def _connect(user, password):
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "ragdb"),
        user=user,
        password=password,
    )


def get_app_conn():
    """Low-privilege user. RLS idha bypass panna mudiyaadhu."""
    return _connect(os.getenv("DB_APP_USER"), os.getenv("DB_APP_PASSWORD"))


def get_admin_conn():
    """Ingest mathiri admin velaikku mattum."""
    return _connect(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"))