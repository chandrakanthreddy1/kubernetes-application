from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

conn = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    dbname=POSTGRES_DB
)

@app.route("/result")
def result():
    cur = conn.cursor()
    cur.execute("SELECT option, votes FROM results")
    rows = cur.fetchall()
    total = sum(v[1] for v in rows) or 1
    result_dict = {opt: f"{(votes/total)*100:.2f}%" for opt, votes in rows}
    return jsonify(result_dict)

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)