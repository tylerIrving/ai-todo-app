from flask import Flask, request, make_response, redirect, url_for
from lib import redis_client, generate_unique_id, add_todo_item, get_todo_items
import pyvibe as pv
import os

app = Flask(__name__)
app.secret_key = os.urandom(32).hex()


@app.route("/")
def index():
    footer = pv.Footer(
        title="Made with ❤️ by Tyler Irving",
        subtitle="",
        link="https://www.linkedin.com/in/tyler-irving-94b567189/",
    )
    navbar = pv.Navbar(
        title="Todo App",
    )
    page = pv.Page("Home", footer=footer, navbar=navbar)
    page.add_header("Todo App")

    # TODO: session id doesn't exist after tab is closed
    session_id = request.cookies.get("session_id")

    with page.add_card() as card:
        card.add_header("Todo Input")
    with card.add_form(action="/add_todo", method="POST") as form:
        form.add_formtext(
            label="", name="todo_item", placeholder="Enter your todo here"
        )
        form.add_formsubmit(label="Submit")

    todo_items = get_todo_items(session_id)
    print(todo_items)
    for item in todo_items.values():
        print(item)
        with page.add_card() as card:
            card.add_header(item["item_name"])

    if not session_id or not redis_client.exists(session_id):
        session_id = generate_unique_id()
        response = make_response(page.to_html())
        response.set_cookie("session_id", session_id)
        return response

    return page.to_html()


@app.route("/add_todo", methods=["POST"])
def add_todo():
    session_id = request.cookies.get("session_id")
    add_todo_item(
        session_id,
        {"item_name": request.form.get("todo_item"), "completed": False},
    )
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(port=8000, debug=True)
