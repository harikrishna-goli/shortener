import mysql.connector

# Connect to MySQL running in Docker
conn = mysql.connector.connect(
    host="localhost",  # maps to container port
    port=3306,
    user="devuser",
    password="devpass",
    database="mydb",
)

cursor = conn.cursor()

# Example: create a table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS short_urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    short_code VARCHAR(50) UNIQUE NOT NULL,
    long_url TEXT NOT NULL,
    expires_at DATETIME,
    click_count INT DEFAULT 0,
    owner_id VARCHAR(255),
    last_accessed DATETIME
)
"""
)


conn.commit()
cursor.close()
conn.close()
