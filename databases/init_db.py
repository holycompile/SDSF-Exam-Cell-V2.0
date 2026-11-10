import sys
from pathlib import Path

# Add project root to sys.path so we can import from databases.connections
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from databases.connections import get_connection


def initialize_database():
    schema_file = current_dir / "schema.sql"

    if not schema_file.exists():
        print(f"❌ Error: schema.sql file not found at {schema_file}")
        return

    # Read the SQL statements from schema.sql
    with open(schema_file, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Split into individual SQL commands by semicolon
    statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]

    if not statements:
        print("⚠️ Warning: schema.sql is empty. Add your CREATE TABLE queries first!")
        return

    print(f"Connecting to TiDB Cloud... Executing {len(statements)} SQL commands.")

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)
            conn.commit()

        print("✅ All tables created and verified successfully in TiDB Cloud!")

        # Verify and display all tables currently in the database
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print("\n📋 Verified tables currently in TiDB Cloud:")
            for t in tables:
                table_name = list(t.values())[0]
                print(f"  • {table_name}")

        conn.close()

    except Exception as err:
        print(f"❌ Database initialization failed: {err}")


if __name__ == "__main__":
    initialize_database()