import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps
from datetime import datetime
from sqlalchemy import desc
from flask import render_template, request, flash, redirect, url_for, session
from app import app, db
from app.models import Message, User, WeightRecord, CholesterolRecord, ExerciseRecord


def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()


def generate_id():
    return secrets.token_urlsafe(50)


def check_cholesterol_level(user):
    user_age = int((datetime.now() - user.dob).days / 365)
    cholesterol = CholesterolRecord.query.filter_by(
        user_id=user.id).order_by(desc("record_date")).first()

    if cholesterol == None:
        return None
    else:
        cholesterol = cholesterol.cholesterol

    if user_age <= 19:
        if cholesterol < 170:
            return "low"
        elif cholesterol >= 200:
            return "high"
        else:
            return "okay"
    if user_age >= 20:
        if cholesterol < 200:
            return "low"
        elif cholesterol >= 239:
            return "high"
        else:
            return "okay"


def check_bmi_level(user):
    bmi = WeightRecord.query.filter_by(
        user_id=user.id).order_by(desc("record_date")).first()

    if bmi == None:
        return None
    else:
        bmi = float(bmi.bmi)
        if bmi < 16:
            return "Severe Thinness"
        if bmi >= 16 and bmi < 17:
            return "Moderate Thinness"
        if bmi >= 17 and bmi < 18.5:
            return "Mild Thinness"
        if bmi >= 18.5 and bmi < 25:
            return "Normal"
        if bmi >= 25 and bmi < 30:
            return "Overweight"
        if bmi >= 30 and bmi < 35:
            return "Obese Class I"
        if bmi >= 35 and bmi < 40:
            return "Obese Class II"
        if bmi >= 40:
            return "Obese Class III"


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        user = User.query.get(session["user"])
        return f(user, *args, **kwargs)
    return decorated


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name").strip().capitalize()
        last_name = request.form.get("last_name").strip().capitalize()
        email = request.form.get("email").strip().lower()
        gender = request.form.get("gender").strip()
        dob = request.form.get("dob").strip()
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        if password != password_confirm:
            flash("The passwords provided do not match", "danger")
            return redirect(url_for("register"))
        if User.query.filter_by(email=email).first():
            flash("The account you are trying to create already exists", "danger")
            return redirect(url_for("register"))

        user = User(id=generate_id(), first_name=first_name, last_name=last_name, email=email,
                    gender=gender, dob=datetime.strptime(dob, "%Y-%m-%d"), password=hash_password(password))
        db.session.add(user)
        db.session.commit()

        flash("Your account has been created, proceed to login", "success")
        return redirect(url_for("register"))
    return render_template("register.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email").strip().lower()
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email, password=hash_password(password)).first()
        if user:
            session["user"] = user.id
            return redirect(url_for("dashboard"))
        else:
            flash("You have supplied incorrect login credentials")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/contact/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        first_name = request.form.get("first_name").strip().capitalize()
        last_name = request.form.get("last_name").strip().capitalize()
        email = request.form.get("email").strip().lower()
        message = request.form.get("message").strip()

        user_message = Message(
            first_name=first_name, last_name=last_name, email=email, message=message)
        db.session.add(user_message)
        db.session.commit()

        flash("Your message has been received and we will get back to you shortly")
        return redirect(url_for("contact"))
    return render_template("contact.html")


@app.route("/reset-password/", methods=["GET", "POST"])
def reset_password():
    return render_template("reset-password.html")


@app.route("/")
@app.route("/dashboard/")
@login_required
def dashboard(user):
    return render_template("dashboard.html", user=user)


@app.route("/dashboard/weight-management/", methods=["GET", "POST"])
@login_required
def weight_management(user):
    if request.method == "POST":
        try:
            height = request.form.get("height").split("'")
            inches = (int(height[0]) * 12) + int(height[1])
            weight = float(request.form.get("weight"))
            calorie_intake = float(request.form.get("calorie_intake"))
            date = datetime.strptime(request.form.get("date"), "%Y-%m-%d")
            WeightRecord.query.filter_by(record_date=date).delete()
            db.session.add(WeightRecord(id=generate_id(), user_id=user.id, height=inches,
                                        weight=weight, calories=calorie_intake, record_date=date))
            db.session.commit()
            flash("Successfully recorded weight data for {}".format(
                str(date).split()[0]), "success")
            return redirect(url_for("weight_management"))
        except:
            flash("An error occured while trying to save your weight data", "danger")
            return redirect(url_for("weight_management"))
    last_record = WeightRecord.query.filter_by(
        user_id=user.id).order_by(desc("record_date")).first()
    if last_record == None:
        last_record = {
            "bmi": "Data Not Available",
            "weight": "Data Not Available",
            "height": "Data Not Available"
        }
    else:
        last_record.bmi = "{:.2f}".format(last_record.bmi)
    return render_template("weight-management.html", user=user, last_record=last_record, bmi=check_bmi_level(user))


@app.route("/dashboard/cholesterol-management/", methods=["GET", "POST"])
@login_required
def cholesterol_management(user):
    if request.method == "POST":
        try:
            hdl_cholesterol = request.form.get("hdl_cholesterol")
            ldl_cholesterol = request.form.get("ldl_cholesterol")
            if hdl_cholesterol == "":
                hdl_cholesterol = None
            else:
                hdl_cholesterol = float(hdl_cholesterol)
            if ldl_cholesterol == "":
                ldl_cholesterol = None
            else:
                ldl_cholesterol = float(ldl_cholesterol)

            cholesterol = float(request.form.get("cholesterol"))
            exercises = int(request.form.get("exercises"))
            target = float(request.form.get("target"))
            date = datetime.strptime(request.form.get("date"), "%Y-%m-%d")
            CholesterolRecord.query.filter_by(record_date=date).delete()
            db.session.add(CholesterolRecord(id=generate_id(), user_id=user.id, cholesterol=cholesterol,
                                             hdl=hdl_cholesterol, ldl=ldl_cholesterol, exercises=exercises, target=target, record_date=date))
            db.session.commit()
            flash("Successfully recorded cholesterol data for {}".format(
                str(date).split()[0]), "success")
            return redirect(url_for("cholesterol_management"))
        except:
            flash("An error occured while trying to save your cholesterol data", "danger")
            return redirect(url_for("cholesterol_management"))
    return render_template("cholesterol-management.html", user=user, cholesterol=check_cholesterol_level(user))


@app.route("/dashboard/exercise-capture/", methods=["GET", "POST"])
@login_required
def exercise_capture(user):
    if request.method == "POST":
        try:
            exercises = int(request.form.get("exercises"))
            date = datetime.strptime(request.form.get("date"), "%Y-%m-%d")
            ExerciseRecord.query.filter_by(record_date=date).delete()
            db.session.add(ExerciseRecord(
                id=generate_id(), user_id=user.id, exercises=exercises, record_date=date))
            db.session.commit()
            flash("Successfully recorded exercise data for {}".format(
                str(date).split()[0]), "success")
            return redirect(url_for("exercise_capture"))
        except:
            flash("An error occured while trying to save your exercise data", "danger")
            return redirect(url_for("exercise_capture"))
    last_record = list(ExerciseRecord.query.filter_by(
        user_id=user.id).order_by(desc("record_date")).limit(2))
    return render_template("exercise-management.html", user=user, last_record=last_record)


@app.route("/dashboard/advisory/")
@login_required
def advisory(user):
    return render_template("advisory.html", user=user, cholesterol=check_cholesterol_level(user), bmi=check_bmi_level(user))


@app.route("/dashboard/weight-records/")
@login_required
def weight_records(user):
    records = WeightRecord.query.filter_by(
        user_id=user.id).order_by(desc("record_date"))
    return render_template("weight-records.html", user=user, records=records)


@app.route("/dashboard/cholesterol-records/")
@login_required
def cholesterol_records(user):
    records = CholesterolRecord.query.filter_by(
        user_id=user.id).order_by(desc("record_date"))
    return render_template("cholesterol-records.html", user=user, records=records)


@app.route("/dashboard/compare/")
@login_required
def compare(user):
    bmi, weight, cholesterol, exercises = [], [], [], []
    for i in WeightRecord.query.filter(WeightRecord.user_id == user.id, WeightRecord.record_date >= datetime.utcnow() - timedelta(days=7)).order_by(desc("record_date")):
        bmi.append([i.record_date.ctime().split()[0], i.bmi])
        weight.append([i.record_date.ctime().split()[0], i.weight])
    for i in CholesterolRecord.query.filter(CholesterolRecord.user_id == user.id, CholesterolRecord.record_date >= datetime.utcnow() - timedelta(days=7)).order_by(desc("record_date")):
        cholesterol.append([i.record_date.ctime().split()[0], i.cholesterol])
    for i in ExerciseRecord.query.filter(ExerciseRecord.user_id == user.id, ExerciseRecord.record_date >= datetime.utcnow() - timedelta(days=7)).order_by(desc("record_date")):
        exercises.append([i.record_date.ctime().split()[0], i.exercises])
    return render_template("compare.html", user=user, bmi=bmi[::-1], weight=weight[::-1], cholesterol=cholesterol[::-1], exercises=exercises[::-1])


@app.route("/dashboard/logout/")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
