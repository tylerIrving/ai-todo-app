from flask import Flask, request, redirect, url_for
from lib import (
    generate_unique_id,
    add_todo_item,
    get_todo_items,
    update_todo_item_ai,
    update_todo_item_complete,
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
    for key, value in todo_items.items():
        if value.get("completed") is False:
            with page.add_card() as card:
                card.add_header(f"Todo Item: {value.get('item_name', '')}")
                if value.get("ai_help") is not None:
                    card.add_text(f"AI Help: {value.get('ai_help')}")
            with card.add_form(action="/generate", method="POST") as form:
                form.add_formhidden(name="session_id", value=session_id)
                form.add_formhidden(name="todo_item_id", value=key)
                form.add_formhidden(name="todo_item", value=value.get("item_name", ""))
                form.add_formsubmit(label="Generate Help")
                card.add_divider()
            with card.add_form(action="/complete", method="POST") as form:
                form.add_formhidden(name="session_id", value=session_id)
                form.add_formhidden(name="todo_item_id", value=key)
                form.add_formhidden(name="todo_item", value=value.get("item_name", ""))
                form.add_formsubmit(label="Complete Todo")

    return page.to_html()


@app.route("/complete", methods=["POST"])
def complete_todo_help():
    session_id = request.form.get("session_id")
    todo_item = request.form.get("todo_item")
    todo_item_id = request.form.get("todo_item_id")
    update_todo_item_complete(
        session_id, todo_item_id, {"item_name": todo_item, "completed": True}
    )

    return redirect(url_for("index", session_id=session_id))


@app.route("/generate", methods=["POST"])
def generate_todo_help():
    session_id = request.form.get("session_id")
    todo_item = request.form.get("todo_item")
    todo_item_id = request.form.get("todo_item_id")
    update_todo_item_ai(
        session_id, todo_item_id, {"item_name": todo_item, "completed": False}
    )

    return redirect(url_for("index", session_id=session_id))


if __name__ == "__main__":
    app.run(port=8000, debug=True)
