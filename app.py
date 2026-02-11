from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()

        if user:
            session["user_id"] = user[0]
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?)", (name, email, password))
        db.commit()

        return redirect("/")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    filter_type = request.args.get("filter", "all")

    db = get_db()
    cur = db.cursor()

    # Get username
    cur.execute("SELECT name FROM users WHERE id=?", (session["user_id"],))
    user = cur.fetchone()

    # Get tasks based on filter
    if filter_type == "completed":
        cur.execute(
            "SELECT * FROM tasks WHERE user_id=? AND completed=1",
            (session["user_id"],)
        )
    elif filter_type == "pending":
        cur.execute(
            "SELECT * FROM tasks WHERE user_id=? AND completed=0",
            (session["user_id"],)
        )
    else:
        cur.execute(
            "SELECT * FROM tasks WHERE user_id=?",
            (session["user_id"],)
        )

    raw_tasks = cur.fetchall()

    # Deadline status logic
    task_data = []
    today = datetime.today().date()

    for task in raw_tasks:
        deadline_date = datetime.strptime(task[3], "%Y-%m-%d").date()
        days_left = (deadline_date - today).days

        if days_left < 0:
            status = "overdue"
        elif days_left <= 3:
            status = "due"
        else:
            status = "ontrack"

        task_data.append(task + (status,))

    # Progress calculation (from ALL tasks)
    cur.execute("SELECT * FROM tasks WHERE user_id=?", (session["user_id"],))
    all_tasks = cur.fetchall()

    completed = len([t for t in all_tasks if t[4] == 1])
    total = len(all_tasks)
    progress = int((completed / total) * 100) if total > 0 else 0

    return render_template(
        "dashboard.html",
        tasks=task_data,
        progress=progress,
        username=user[0],
        completed=completed,
        pending=total - completed,
        filter_type=filter_type
    )

@app.route("/add_task", methods=["POST"])
def add_task():
    title = request.form["title"]
    deadline = request.form["deadline"]

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO tasks VALUES (NULL, ?, ?, ?, 0)", (session["user_id"], title, deadline))
    db.commit()

    return redirect("/dashboard")

@app.route("/complete/<int:id>")
def complete(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE tasks SET completed=1 WHERE id=?", (id,))
    db.commit()
    return redirect("/dashboard")
@app.route("/delete/<int:id>")
def delete(id):
    if "user_id" not in session:
        return redirect("/")

    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    db.commit()
    return redirect("/dashboard")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if "user_id" not in session:
        return redirect("/")

    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        title = request.form["title"]
        deadline = request.form["deadline"]

        cur.execute(
            "UPDATE tasks SET title=?, deadline=? WHERE id=?",
            (title, deadline, id)
        )
        db.commit()
        return redirect("/dashboard")

    # GET request → load existing task
    cur.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = cur.fetchone()

    return render_template("edit_task.html", task=task)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

app.run(debug=True)
