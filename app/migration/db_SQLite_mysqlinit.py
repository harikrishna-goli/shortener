import sqlite3
import mysql.connector
from datetime import datetime

# --- Step 1: Connect to SQLite ---
sqlite_conn = sqlite3.connect("shortener.db")  # adjust path if needed according the place you running from
sqlite_cursor = sqlite_conn.cursor()

# Read all rows from SQLite table
sqlite_cursor.execute("SELECT short_code, long_url, expires_at, click_count, owner_id, last_accessed FROM short_urls")
rows = sqlite_cursor.fetchall()
print(f"Fetched {len(rows)} rows from SQLite.")

# --- Step 2: Connect to MySQL ---
mysql_conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="devuser",
    password="devpass",
    database="mydb"
)
mysql_cursor = mysql_conn.cursor()

# --- Step 3: Create MySQL table if not exists ---
mysql_cursor.execute("""
CREATE TABLE IF NOT EXISTS short_urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    short_code VARCHAR(50) UNIQUE NOT NULL,
    long_url TEXT NOT NULL,
    expires_at DATETIME,
    click_count INT DEFAULT 0,
    owner_id VARCHAR(255),
    last_accessed DATETIME
)
""")

# --- Step 4: Insert rows into MySQL ---
for row in rows:
    short_code, long_url, expires_at, click_count, owner_id, last_accessed = row

    # Convert timestamps if needed
    def parse_datetime(dt):
        if isinstance(dt, str):
            try:
                return datetime.fromisoformat(dt)
            except ValueError:
                return None
        return dt

    mysql_cursor.execute("""
        INSERT INTO short_urls (short_code, long_url, expires_at, click_count, owner_id, last_accessed)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        short_code,
        long_url,
        parse_datetime(expires_at),
        click_count,
        owner_id,
        parse_datetime(last_accessed)
    ))

mysql_conn.commit()
print(f"Inserted {len(rows)} rows into MySQL.")

# --- Step 5: Close connections ---
sqlite_cursor.close()
sqlite_conn.close()
mysql_cursor.close()
mysql_conn.close()
print("✅ Migration completed successfully!")
