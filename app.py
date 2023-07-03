from flask import Flask, request
from lib import (
    generate_unique_id,
    add_todo_item,
    get_todo_items,
    todo_item_help,
)
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
    session_id = request.args.get("session_id")
    todo_item = request.args.get("todo_item")

    if not session_id:
        session_id = generate_unique_id()

    if todo_item:
        add_todo_item(session_id, {"item_name": todo_item, "completed": False})

    with page.add_card() as card:
        card.add_header("Todo Input")
    with card.add_form(action="/") as form:
        form.add_formtext(
            label="", name="todo_item", placeholder="Enter your todo here"
        )
        form.add_formhidden(name="session_id", value=session_id)
        form.add_formsubmit(label="Add Todo")

    todo_items = get_todo_items(session_id)
    for item in todo_items.values():
        todo_help = todo_item_help(item["item_name"])
        with page.add_card() as card:
            card.add_header(item["item_name"])
            card.add_text(todo_help)

    return page.to_html()


if __name__ == "__main__":
    app.run(port=8000, debug=True)
