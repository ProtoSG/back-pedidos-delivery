from sqlalchemy import create_engine
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
        TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

        dbUrl = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"
        engine = create_engine(dbUrl, connect_args={'check_same_thread': False}, echo=True)
        session = Session(engine)
        print("Obteniendo session")
        if(session):
            print("Si hay")

        return session
    except Exception as ex:
        return None
