from datetime import datetime
from sqlalchemy.orm import column_property
from app import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    resolved = db.Column(db.Boolean, nullable=False, default=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class User(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class WeightRecord(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    bmi = column_property((weight / height / height) * 703)
    record_date = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class CholesterolRecord(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    cholesterol = db.Column(db.Float, nullable=False)
    hdl = db.Column(db.Float, nullable=True)
    ldl = db.Column(db.Float, nullable=True)
    exercises = db.Column(db.Integer, nullable=False)
    target = db.Column(db.Float, nullable=False)
    record_date = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class ExerciseRecord(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    exercises = db.Column(db.Integer, nullable=False)
    record_date = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
