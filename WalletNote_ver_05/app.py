# WalletNote_ver_05/app.py
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
)

from WalletNote_ver_05.Backend.Database.CreateDB import CreateDB
from WalletNote_ver_05.Backend.Database.RecordDB import RecordDB
from WalletNote_ver_05.Backend.Information.InputUserInformation import UserInformation
from WalletNote_ver_05.Backend.Information.InputInformation import InputInformation
from WalletNote_ver_05.Backend.System.Dashboard import Dashboard
from WalletNote_ver_05.Backend.System.OCR_System import OCRSystem
from WalletNote_ver_05.Backend.System.Setting import Setting

# ---------------------------------------------------------------------
# Flask App Configuration  ★★★ ここが修正点 ★★★
# ---------------------------------------------------------------------

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)
app.secret_key = "walletnote_secret_key"

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------
# Initial DB Setup
# ---------------------------------------------------------------------

def initialize_database() -> None:
    creator = CreateDB()
    creator.initialize_all()

initialize_database()

# ---------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------

def get_current_user() -> UserInformation | None:
    if "username" not in session or "email" not in session:
        return None
    return UserInformation(
        username=session["username"],
        email=session["email"],
    )

# ---------------------------------------------------------------------
# Routes - Pages
# ---------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/signup")
def signup_page():
    return render_template("signup.html")


@app.route("/dashboard")
def dashboard_page():
    user = get_current_user()
    if user is None:
        return redirect(url_for("login_page"))

    dashboard = Dashboard()
    data = dashboard.load_dashboard(user)

    return render_template(
        "dashboard.html",
        records=data["records"],
        graphs=data["graphs"],
    )


@app.route("/setting")
def setting_page():
    user = get_current_user()
    if user is None:
        return redirect(url_for("login_page"))

    setting = Setting()
    currency = setting.get_currency(user)

    return render_template("setting.html", currency=currency)

# ---------------------------------------------------------------------
# Routes - Auth API
# ---------------------------------------------------------------------
@app.route("/api/signup", methods=["POST"])
def api_signup():
    try:
        data = request.get_json(force=True)

        user = UserInformation(
            username=data["username"],
            email=data["email"],
        )
        user.validate()
        user.set_password(data["password"])

        db = RecordDB()
        db.connect()

        sql = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        """
        db.execute(sql, (user.username, user.email, user.password_hash))
        db.commit()
        db.close()

        session["username"] = user.username
        session["email"] = user.email

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400



@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json

    db = RecordDB()
    sql = """
    SELECT username, email, password_hash
    FROM users
    WHERE username = %s
    """
    row = db.fetch_one(sql, (data["username"],))

    if not row:
        return jsonify({"success": False}), 401

    user = UserInformation(
        username=row["username"],
        email=row["email"],
        _password_hash=row["password_hash"],
    )

    if not user.verify_password(data["password"]):
        return jsonify({"success": False}), 401

    session["username"] = user.username
    session["email"] = user.email

    return jsonify({"success": True})


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"success": True})

# ---------------------------------------------------------------------
# Routes - Record API
# ---------------------------------------------------------------------

@app.route("/api/record", methods=["POST"])
def api_record():
    user = get_current_user()
    if user is None:
        return jsonify({"success": False}), 401

    data = request.json

    record = InputInformation(
        price=Decimal(data["price"]),
        date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
        service_or_product=data["service"],
    )

    RecordDB().insert_record(user, record)

    return jsonify({"success": True})


@app.route("/api/ocr", methods=["POST"])
def api_ocr():
    user = get_current_user()
    if user is None:
        return jsonify({"success": False}), 401

    file = request.files["image"]
    image_path = UPLOAD_DIR / file.filename
    file.save(image_path)

    ocr = OCRSystem()
    record = ocr.process_and_save(str(image_path), user)

    return jsonify(
        {
            "success": True,
            "price": float(record.price),
            "date": record.date.isoformat(),
            "service": record.service_or_product,
        }
    )

# ---------------------------------------------------------------------
# Routes - Setting API
# ---------------------------------------------------------------------

@app.route("/api/setting/currency", methods=["POST"])
def api_set_currency():
    user = get_current_user()
    if user is None:
        return jsonify({"success": False}), 401

    data = request.json
    setting = Setting()
    setting.set_currency(user, data["currency"])

    return jsonify({"success": True})

# ---------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
