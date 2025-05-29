import os
import pytest
import sqlite3

TEST_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'test.db')
DB_SQL_PATH = os.path.join(os.path.dirname(__file__), '..', 'src', 'database', 'db.sql')

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Elimina test.db si existe antes de los tests
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    # Crea una nueva base de datos y ejecuta db.sql para crear las tablas
    conn = sqlite3.connect(TEST_DB_PATH)
    with open(DB_SQL_PATH, "r", encoding="utf-8") as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.close()
    # Setea la variable de entorno para que la app use test.db
    os.environ["TURSO_DATABASE_URL"] = f"file:{TEST_DB_PATH}"
    os.environ["TURSO_AUTH_TOKEN"] = ""
    yield
    # Limpia test.db después de los tests
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
