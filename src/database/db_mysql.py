import os
from dotenv import load_dotenv
import libsql_experimental as libsql

def get_connection():
    try:
        load_dotenv()
        url = os.environ.get("TURSO_DATABASE_URL")
        auth_token = os.environ.get("TURSO_AUTH_TOKEN")

        session = libsql.connect(database=url, auth_token=auth_token)

        return session
    except Error:
        print("Error: ", Error)
