import time

from flask import Flask

from job import run
from modules import delete_old_pages

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Book scraper is running"


@app.route("/add-to-notion", methods=["GET", "POST"])
def run_add_notion():
    try:
        delete_old_pages()
        time.sleep(5)
        run()
        return "Notion update is done", 200
    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
