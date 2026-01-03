from flask import Flask, request, render_template_string
import redis
import os

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

HTML = """
<h1>Vote</h1>
<form method="POST">
  <button name="vote" value="cat">🐱 Cat</button>
  <button name="vote" value="dog">🐶 Dog</button>
</form>
"""

@app.route("/vote", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        vote_choice = request.form["vote"]
        r.incr(vote_choice)
    return render_template_string(HTML)

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
