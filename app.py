from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = "routinebattle123"

init_db()
@app.route("/")
def home():
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()

    routines = conn.execute(
        "SELECT * FROM routines WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    total = len(routines)

    completed = sum(
        routine["completed"]
        for routine in routines
    )
    streak = 0
    progress = 0

    if total > 0:
        progress = round(
            (completed / total) * 100
        )

    conn.close()

    # return render_template(
    #     "dashboard.html",
    #     routines=routines,
    #     progress=progress
    # )

    return render_template(
    "dashboard.html",
    routines=routines,
    progress=progress,
    total=total,
    completed=completed,
    streak=streak
)



@app.route("/add_routine", methods=["POST"])
def add_routine():

    task = request.form["task"]

    if task.strip():

        conn = get_db_connection()

        conn.execute(
            "INSERT INTO routines (user_id, task_name) VALUES (?, ?)",
            (session["user_id"], task)
        )

        conn.commit()
        conn.close()

    return redirect("/dashboard")
@app.route("/toggle/<int:id>")
def toggle_task(id):

    conn = get_db_connection()

    routine = conn.execute(
        "SELECT completed FROM routines WHERE id=?",
        (id,)
    ).fetchone()

    new_value = 0 if routine["completed"] else 1

    conn.execute(
        "UPDATE routines SET completed=? WHERE id=?",
        (new_value, id)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/delete/<int:id>")
def delete_task(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM routines WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO users
            (username,email,password)
            VALUES (?,?,?)
            """,
            (username,email,hashed_password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]

            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)