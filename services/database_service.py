import sqlite3


DATABASE_PATH = "chat.db"


def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH
    )

    return connection


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    # -------------------------
    # Messages table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    # -------------------------
    # Users table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # -------------------------
    # Add role column if missing
    # -------------------------

    cursor.execute(
        "PRAGMA table_info(users)"
    )

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if "role" not in columns:
        cursor.execute(
            """
            ALTER TABLE users
            ADD COLUMN role TEXT NOT NULL
            DEFAULT 'employee'
            """
        )

    # -------------------------
    # Save changes
    # -------------------------

    connection.commit()
    connection.close()