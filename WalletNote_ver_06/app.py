from __future__ import annotations

from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from Backend.Database.CreateDB import CreateDB
from Backend.Database.RecordDB import RecordDB
from Backend.Database.ConnectDB import ConnectDB
from Backend.System.Dashboard import Dashboard
from Backend.System.OCR_System import OCRSystem
from Backend.System.Setting import Setting
from Backend.Information.InputUserInformation import UserInformation
from Backend.Information.InputInformation import InputInformation

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "frontend/templates"),
    static_folder=str(BASE_DIR / "frontend/static"),
)
app.secret_key = "walletnote_secret"

# =========================
# DB Initialize (SAFE)
# =========================
CreateDB().initialize()


# =========================
# Utils
# =========================
def get_current_user() -> UserInformation | None:
    if "user_id" not in session:
        return None

    return UserInformation(
        user_id=session["user_id"],
        username=session["username"],
        email=session["email"],
    )


# =========================
# Routes
# =========================
@app.route("/")
def index():
    return render_template("index.html")


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = request.get_json(force=True)

    db = ConnectDB()
    row = db.fetch_one(
        "SELECT id, username, email FROM users WHERE email=%s AND password=%s",
        (data["email"], data["password"]),
    )

    if not row:
        return jsonify(success=False), 401

    session["user_id"], session["username"], session["email"] = row
    return jsonify(success=True)


# ---------- SIGNUP ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    data = request.get_json(force=True)
    db = ConnectDB()

    # email duplicate check
    exists = db.fetch_one(
        "SELECT id FROM users WHERE email=%s",
        (data["email"],),
    )
    if exists:
        return jsonify(success=False), 409

    db.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (data["username"], data["email"], data["password"]),
    )

    user_id = db.fetch_one(
        "SELECT id FROM users WHERE email=%s",
        (data["email"],),
    )[0]

    session["user_id"] = user_id
    session["username"] = data["username"]
    session["email"] = data["email"]

    return jsonify(success=True)


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    dash = Dashboard()
    return render_template(
        "dashboard.html",
        data={
            "recent": dash.get_recent_records(user.user_id),
            "balance": dash.calculate_balance(user.user_id),
            "today": dash.today_summary(user.user_id),
        },
    )


# ---------- EXPENSE ----------
@app.route("/record/expense", methods=["POST"])
def record_expense():
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized"), 401

    data = request.get_json(force=True)
    record = InputInformation(
        price=data["price"],
        service=data["service"],
        record_date=data["date"],
    )

    RecordDB().add_record(user, record, "expense")
    return jsonify(success=True)


# ---------- INCOME ----------
@app.route("/record/income", methods=["POST"])
def record_income():
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized"), 401

    data = request.get_json(force=True)
    record = InputInformation(
        price=data["price"],
        service=data["service"],
        record_date=data["date"],
    )

    RecordDB().add_record(user, record, "income")
    return jsonify(success=True)


# ---------- OCR ----------
@app.route("/record/ocr", methods=["POST"])
def record_ocr():
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized"), 401

    image = request.files["image"]
    path = UPLOAD_DIR / image.filename
    image.save(path)

    OCRSystem().process_image(user, path)
    return jsonify(success=True)


# ---------- SETTINGS ----------
@app.route("/setting")
def setting():
    if not get_current_user():
        return redirect(url_for("login"))
    return render_template("setting.html")


@app.route("/setting/save", methods=["POST"])
def save_setting():
    user = get_current_user()
    if not user:
        return jsonify(error="unauthorized"), 401

    data = request.get_json(force=True)
    Setting(user).set_currency(data["currency"])
    return jsonify(success=True)


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/api/chart/summary")
def chart_summary():
    user = get_current_user()
    if not user:
        return jsonify({}), 401

    dash = Dashboard()
    return jsonify(dash.get_summary_by_type(user.user_id))


@app.route("/api/chart/expense")
def chart_expense():
    user = get_current_user()
    if not user:
        return jsonify([]), 401

    dash = Dashboard()
    return jsonify(dash.get_expense_by_service(user.user_id))


# =========================
# Run
# =========================
if __name__ == "__main__":
    app.run(debug=True)
