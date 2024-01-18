from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError

from flask import Blueprint, jsonify, request

from app.models import Balance, Expense, User, db
from app.tasks import send_expense_notification

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


def calculate_expense(payload):
    try:
        participants = User.query.filter(
            User.user_id.in_(payload.get("participants"))
        ).all()
        total_participants = len(participants)
        amount = payload.get("amount")
        user_amount = {}

        if payload.get("type") == "EQUAL":
            for participant in participants:
                shared_amount = round(amount / total_participants, 2)
                balance = Balance(
                    creditor_id=payload.get("payer"),
                    debitor_id=participant.user_id,
                    amount=shared_amount,
                )
                db.session.add(balance)
                user_amount[participant.user_id] = shared_amount
        elif payload.get("type") == "EXACT":
            for share in payload.get("shares"):
                debitor_id = share.get("user_id")
                shared_amount = round(share.get("amount"), 2)
                balance = Balance(
                    creditor_id=payload.get("payer"),
                    debitor_id=debitor_id,
                    amount=shared_amount,
                )
                db.session.add(balance)
                user_amount[debitor_id] = shared_amount
        elif payload.get("type") == "PERCENT":
            total_percent = sum(share.get("percent")
                                for share in payload.get("shares"))
            if total_percent != 100:
                raise ValueError("Total percentage shares must equal 100.")
            for share in payload.get("shares"):
                debitor_id = share.get("user_id")
                shared_amount = round(
                    ((amount * share.get("percent")) / 100), 2)
                balance = Balance(
                    creditor_id=payload.get("payer"),
                    debitor_id=debitor_id,
                    amount=shared_amount,
                )
                db.session.add(balance)
                user_amount[debitor_id] = shared_amount

        expense = Expense(
            amount=payload.get("amount"),
            payer_id=payload.get("payer"),
            expense_type=payload.get("type"),
        )
        db.session.add(expense)

        for participant in participants:
            simplify_balances(participant.user_id)

        db.session.commit()
        expense_notification_sender(
            participants, user_amount, payload.get("payer"))
        return True

    except SQLAlchemyError as db_error:
        db.session.rollback()
        print(f"Database Error: {db_error}")
        return False
    except ValueError as value_error:
        db.session.rollback()
        print(f"Value Error: {value_error}")
        return False


def simplify_balances(user_id):
    balances = Balance.query.filter(
        (Balance.creditor_id == user_id) | (Balance.debitor_id == user_id)
    ).all()
    user = User.query.get(user_id)
    user.balance = 0
    for balance in balances:
        if balance.creditor_id != balance.debitor_id:
            if balance.creditor_id == user_id:
                user.balance += balance.amount
            elif balance.debitor_id == user_id:
                user.balance -= balance.amount
    db.session.flush()


def expense_notification_sender(participants, user_amount, payer_id):
    try:
        user = User.query.get(payer_id)
        for participant in participants:
            if participant.user_id in user_amount:
                send_expense_notification.delay(
                    participant.email,
                    user_amount[participant.user_id],
                    user.name
                )
    except Exception as ex:
        print(f"Error Occured: {ex}")
