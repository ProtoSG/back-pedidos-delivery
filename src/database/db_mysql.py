import os
from dotenv import load_dotenv
import libsql_experimental as libsql

def get_connection():
    try:
        load_dotenv()
        url = os.environ.get("TURSO_DATABASE_URL")
        auth_token = os.environ.get("TURSO_AUTH_TOKEN")

        # Si la URL es local (file:), no pases auth_token
        if url and url.startswith("file:"):
            session = libsql.connect(url)
        else:
            session = libsql.connect(database=url, auth_token=auth_token)

        return session
    except Exception as e:
        print("Error en get_connection:", e)
        raise
