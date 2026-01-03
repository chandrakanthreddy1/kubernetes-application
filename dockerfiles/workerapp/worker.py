import redis
import psycopg2
import os
import time

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
conn = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    dbname=POSTGRES_DB
)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS results (
    option TEXT PRIMARY KEY,
    votes INT
)
""")
conn.commit()

print("Worker started...")

while True:
    for option in ["cat", "dog"]:
        count = int(r.get(option) or 0)
        cur.execute("""
        INSERT INTO results(option, votes)
        VALUES (%s, %s)
        ON CONFLICT (option)
        DO UPDATE SET votes = EXCLUDED.votes
        """, (option, count))
    conn.commit()
    time.sleep(5)
