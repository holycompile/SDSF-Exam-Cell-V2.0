import os
import pymysql
from dotenv import load_dotenv
from pathlib import Path

# Load variables from the root .env file (override=True ensures it overrides Windows system variables)
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

def get_connection():
    """
    Establishes and returns a connection to TiDB Cloud.
    """
    return pymysql.connect(
        host=os.getenv("TIDB_HOST"),
        port=int(os.getenv("PORT", 4000)),
        user=os.getenv("TIDB_USER") or os.getenv("USERNAME"),
        password=os.getenv("TIDB_PASS") or os.getenv("PASSWORD"),
        database=os.getenv("DATABASE", "test"),  # Defaults to 'test' if not in .env
        ssl_verify_cert=True,                   # Required for TiDB Cloud SSL
        cursorclass=pymysql.cursors.DictCursor  # Returns rows as Python dictionaries
    )

# --- Test script to verify the connection ---
if __name__ == "__main__":
    print("Testing connection to TiDB Cloud...")
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION() AS tidb_version;")
            result = cursor.fetchone()
            print(" Connected successfully to TiDB Cloud!")
            print("TiDB Version:", result["tidb_version"])
        connection.close()
    except Exception as error:
        print(" Failed to connect to TiDB Cloud:")
        print(error)