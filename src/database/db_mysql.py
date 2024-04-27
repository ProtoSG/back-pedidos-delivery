from decouple import config
import libsql_experimental as libsql

def get_connection():
    try:
        return libsql.connect(
            "delivery",
            sync_url=config("TURSO_DATABASE_URL"),
            auth_token=config("TURSO_AUTH_TOKEN")
        )
    except Exception as ex:
        print(ex)