import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # needed for flash messages

API_URL = "http://127.0.0.1:8000"


def form_to_game(form):
    """Turn the submitted HTML form into the JSON the API expects."""
    return {
        "title": form["title"],
        "platform": form["platform"],
        "hours_played": float(form["hours_played"] or 0),
        "completed": "completed" in form,  # unchecked checkboxes aren't sent
    }


# READ ALL
@app.route("/")
def index():
    response = requests.get(f"{API_URL}/games")
    return render_template("index.html", games=response.json())


# READ ONE
@app.route("/games/<int:game_id>")
def detail(game_id):
    response = requests.get(f"{API_URL}/games/{game_id}")
    if response.status_code == 404:
        flash("Game not found.")
        return redirect(url_for("index"))
    return render_template("detail.html", game=response.json())


# CREATE
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        response = requests.post(f"{API_URL}/games", json=form_to_game(request.form))
        if response.status_code == 201:
            flash("Game added!")
            return redirect(url_for("index"))
        flash("The API rejected that data. Check your inputs.")
    return render_template("form.html", game=None, action="Add")


# UPDATE
@app.route("/edit/<int:game_id>", methods=["GET", "POST"])
def edit(game_id):
    if request.method == "POST":
        response = requests.patch(
            f"{API_URL}/games/{game_id}", json=form_to_game(request.form)
        )
        if response.status_code == 200:
            flash("Game updated!")
            return redirect(url_for("index"))
        flash("The API rejected that data. Check your inputs.")

    response = requests.get(f"{API_URL}/games/{game_id}")
    if response.status_code == 404:
        flash("Game not found.")
        return redirect(url_for("index"))
    return render_template("form.html", game=response.json(), action="Edit")


# DELETE
@app.route("/delete/<int:game_id>", methods=["POST"])
def delete(game_id):
    requests.delete(f"{API_URL}/games/{game_id}")
    flash("Game deleted.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(port=5000, debug=True)