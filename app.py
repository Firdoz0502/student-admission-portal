from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = "student_admission_secret_key"

# ==========================================
# ADMIN LOGIN
# ==========================================

ADMIN_USERNAME = "Firdoz@0205"
ADMIN_PASSWORD = "Mushh@205"

# ==========================================
# DATABASE
# ==========================================

DATABASE = "student.db"

# ==========================================
# UPLOAD FOLDERS
# ==========================================

UPLOAD_FOLDER = "static/uploads"

PHOTO_FOLDER = os.path.join(UPLOAD_FOLDER, "photos")
SSLC_FOLDER = os.path.join(UPLOAD_FOLDER, "sslc")
PUC_FOLDER = os.path.join(UPLOAD_FOLDER, "puc")
AADHAAR_FOLDER = os.path.join(UPLOAD_FOLDER, "aadhaar")
TC_FOLDER = os.path.join(UPLOAD_FOLDER, "tc")

for folder in [
    PHOTO_FOLDER,
    SSLC_FOLDER,
    PUC_FOLDER,
    AADHAAR_FOLDER,
    TC_FOLDER
]:
    os.makedirs(folder, exist_ok=True)

# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# CREATE TABLE
# ==========================================

def init_db():

    conn = get_db()

    conn.execute("""

    CREATE TABLE IF NOT EXISTS students(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fullname TEXT,
        dob TEXT,
        gender TEXT,

        father TEXT,
        mother TEXT,
        phone TEXT,

        nationality TEXT,
        category TEXT,
        blood TEXT,

        sslc_board TEXT,
        sslc_percentage TEXT,
        sslc_year TEXT,

        puc_board TEXT,
        puc_percentage TEXT,
        puc_year TEXT,

        course TEXT,
        shift TEXT,

        photo TEXT,
        sslc TEXT,
        puc TEXT,
        aadhaar TEXT,
        tc TEXT,

        place TEXT,
        declaration_date TEXT

    )

    """)

    conn.commit()
    conn.close()

init_db()

# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("home.html")

# ==========================================
# PERSONAL DETAILS
# ==========================================

@app.route("/personal")
def personal():
    return render_template("personal.html")

# ==========================================
# SAVE PERSONAL DETAILS
# ==========================================

@app.route("/academic", methods=["GET", "POST"])
def academic():

    if request.method == "POST":

        session["fullname"] = request.form.get("fullname")
        session["dob"] = request.form.get("dob")
        session["gender"] = request.form.get("gender")
        session["father"] = request.form.get("father")
        session["mother"] = request.form.get("mother")
        session["phone"] = request.form.get("phone")
        session["nationality"] = request.form.get("nationality")
        session["blood"] = request.form.get("blood")

        return render_template("academic.html")

    return redirect(url_for("personal"))

# ==========================================
# SAVE ACADEMIC DETAILS
# ==========================================

@app.route("/documents", methods=["GET", "POST"])
def documents():

    if request.method == "POST":

        session["sslc_board"] = request.form.get("sslc_board")
        session["sslc_percentage"] = request.form.get("sslc_percentage")
        session["sslc_year"] = request.form.get("sslc_year")

        session["puc_board"] = request.form.get("puc_board")
        session["puc_percentage"] = request.form.get("puc_percentage")
        session["puc_year"] = request.form.get("puc_year")

        session["course"] = request.form.get("course")
        session["shift"] = request.form.get("shift")

        return render_template("documents.html")

    return redirect(url_for("academic"))

# ==========================================
# DOCUMENT UPLOAD + PREVIEW
# ==========================================

@app.route("/preview", methods=["GET", "POST"])
def preview():

    if request.method == "POST":

        uploads = {
            "photo": PHOTO_FOLDER,
            "sslc": SSLC_FOLDER,
            "puc": PUC_FOLDER,
            "aadhaar": AADHAAR_FOLDER,
            "tc": TC_FOLDER
        }

        for field, folder in uploads.items():

            file = request.files.get(field)

            if file and file.filename:

                filename = secure_filename(file.filename)

                file.save(os.path.join(folder, filename))

                session[field] = filename

        return render_template(
            "preview.html",
            data=session
        )

    return redirect(url_for("documents"))

# ==========================================
# DECLARATION PAGE
# ==========================================

@app.route("/declaration", methods=["GET", "POST"])
def declaration():

    if request.method == "POST":
        return render_template("declaration.html")

    return redirect(url_for("preview"))

# ==========================================
# SUBMIT APPLICATION
# ==========================================

@app.route("/submit_application", methods=["POST"])
def submit_application():

    conn = get_db()

    cursor = conn.execute("""

    INSERT INTO students(

        fullname,
        dob,
        gender,

        father,
        mother,
        phone,

        nationality,
        category,
        blood,

        sslc_board,
        sslc_percentage,
        sslc_year,

        puc_board,
        puc_percentage,
        puc_year,

        course,
        shift,

        photo,
        sslc,
        puc,
        aadhaar,
        tc,

        place,
        declaration_date

    )

    VALUES(
        ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?
    )

    """,

    (

        session.get("fullname"),
        session.get("dob"),
        session.get("gender"),

        session.get("father"),
        session.get("mother"),
        session.get("phone"),

        session.get("nationality"),
        session.get("category"),
        session.get("blood"),

        session.get("sslc_board"),
        session.get("sslc_percentage"),
        session.get("sslc_year"),

        session.get("puc_board"),
        session.get("puc_percentage"),
        session.get("puc_year"),

        session.get("course"),
        session.get("shift"),

        session.get("photo"),
        session.get("sslc"),
        session.get("puc"),
        session.get("aadhaar"),
        session.get("tc"),

        request.form.get("place"),
        request.form.get("declaration_date")

    ))

    conn.commit()

    application_id = cursor.lastrowid

    conn.close()

    session.clear()

    return render_template(
        "success.html",
        application_id=application_id
    )

# ==========================================
# ADMIN LOGIN
# ==========================================

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin_logged_in"] = True

            flash("Login Successful!", "success")

            return redirect(url_for("admin_dashboard"))

        else:

            flash("Invalid Username or Password!", "danger")

    return render_template("admin_login.html")

#View Student

@app.route("/view_student/<int:id>")
def view_student(id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "view_student.html",
        student=student
    )
# ==========================================
# ADMIN DASHBOARD
# ==========================================

@app.route("/admin")
def admin_dashboard():

    if not session.get("admin_logged_in"):
        flash("Please login first.", "warning")
        return redirect(url_for("admin_login"))

    conn = get_db()

    # Dashboard Statistics
    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    male_students = conn.execute(
        "SELECT COUNT(*) FROM students WHERE gender='Male'"
    ).fetchone()[0]

    female_students = conn.execute(
        "SELECT COUNT(*) FROM students WHERE gender='Female'"
    ).fetchone()[0]

    # Search
    search = request.args.get("search", "").strip()

    if search:

        students = conn.execute(
            """
            SELECT * FROM students
            WHERE fullname LIKE ?
               OR CAST(id AS TEXT) LIKE ?
            ORDER BY id DESC
            """,
            (f"%{search}%", f"%{search}%")
        ).fetchall()

    else:

        students = conn.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        students=students,
        total_students=total_students,
        male_students=male_students,
        female_students=female_students,
        search=search
    )

# ==========================================
# SEARCH APPLICATION
# ==========================================

@app.route("/search", methods=["GET"])
def search():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    keyword = request.args.get("keyword", "").strip()

    conn = get_db()

    if keyword == "":

        students = conn.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()

    else:

        students = conn.execute("""

        SELECT *

        FROM students

        WHERE

        fullname LIKE ?

        OR course LIKE ?

        OR nationality LIKE ?

        OR category LIKE ?

        """,

        (

            "%" + keyword + "%",
            "%" + keyword + "%",
            "%" + keyword + "%",
            "%" + keyword + "%"

        )

        ).fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        students=students,
        total_students=len(students),
        male_students=sum(1 for s in students if s["gender"] == "Male"),
        female_students=sum(1 for s in students if s["gender"] == "Female")
    )
# ==========================================
# EDIT STUDENT
# ==========================================

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db()

    if request.method == "POST":

        conn.execute("""

        UPDATE students SET

            fullname=?,
            dob=?,
            gender=?,
            father=?,
            mother=?,
            nationality=?,
            category=?,
            blood=?,

            sslc_board=?,
            sslc_percentage=?,
            sslc_year=?,

            puc_board=?,
            puc_percentage=?,
            puc_year=?,

            course=?,
            shift=?,

            place=?,
            declaration_date=?

        WHERE id=?

        """,

        (

            request.form["fullname"],
            request.form["dob"],
            request.form["gender"],
            request.form["father"],
            request.form["mother"],
            request.form["nationality"],
            request.form["category"],
            request.form["blood"],

            request.form["sslc_board"],
            request.form["sslc_percentage"],
            request.form["sslc_year"],

            request.form["puc_board"],
            request.form["puc_percentage"],
            request.form["puc_year"],

            request.form["course"],
            request.form["shift"],

            request.form["place"],
            request.form["declaration_date"],

            id

        ))

        conn.commit()
        conn.close()

        flash("Application Updated Successfully!", "success")

        return redirect(url_for("admin_dashboard"))

    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit.html",
        student=student
    )


# ==========================================
# DELETE STUDENT
# ==========================================

@app.route("/delete/<int:id>")
def delete_student(id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db()

    conn.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Application Deleted Successfully!", "success")

    return redirect(url_for("admin_dashboard"))


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.pop("admin_logged_in", None)

    flash("Logged Out Successfully!", "success")

    return redirect(url_for("admin_login"))


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)