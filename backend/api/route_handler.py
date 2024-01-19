from sqlite3 import IntegrityError

from api.operations import calculate_expense
from app.models import Balance, User, db
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

api_routes = Blueprint("api", __name__)


@api_routes.route("/add/", methods=["POST"])
def add_user():
    try:
        data = request.get_json() or {}
        user = User(
            name=data.get("name"),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(response={"msg": "added successfully"})
    except IntegrityError as integrity_error:
        db.session.rollback()
        print(f"IntegrityError Adding User: {integrity_error}")
        return jsonify({"error": "User with the same email already exists"})


@api_routes.route("/add-expense/", methods=["POST"])
def add_expense():
    try:
        data = request.json
        expense = {
            "amount": data.get("amount"),
            "payer": data.get("payer"),
            "type": data.get("type"),
            "participants": data.get("participants"),
            "shares": data.get("shares", []),
        }
        result = calculate_expense(expense)
        if result:
            return jsonify({"message": "Expense added successfully"})
        return jsonify({"message": "Error Occurred. Contact Tech Team"})
    except IntegrityError as integrity_error:
        db.session.rollback()
        print(f"IntegrityError Adding Expense: {integrity_error}")
        return jsonify(
            {"error": "Integrity error. Duplicate entry or violation of constraints."}
        )


@api_routes.route("/show-balances/<user_id>/", methods=["GET"])
def show_balances(user_id):
    try:
        balances = Balance.query.filter(
            (Balance.creditor_id == user_id) | (Balance.debitor_id == user_id)
        ).all()
        balance_data = [
            {
                "creditor": balance.creditor_id,
                "debitor": balance.debitor_id,
                "amount": balance.amount,
            }
            for balance in balances
        ]
        return jsonify({"balances": balance_data})

    except SQLAlchemyError as db_error:
        db.session.rollback()
        print(f"Database Error: {db_error}")
        return False
