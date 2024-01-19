from app.models import Balance, Expense, User, db
from app.tasks import send_expense_notification
from sqlalchemy.exc import SQLAlchemyError


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
            total_percent = sum(share.get("percent") for share in payload.get("shares"))
            if total_percent != 100:
                raise ValueError("Total percentage shares must equal 100.")
            for share in payload.get("shares"):
                debitor_id = share.get("user_id")
                shared_amount = round(((amount * share.get("percent")) / 100), 2)
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
        expense_notification_sender(participants, user_amount, payload.get("payer"))
        return True

    except SQLAlchemyError as db_error:
        db.session.rollback()
        print(f"Database Error: {db_error}")
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
                    participant.email, user_amount[participant.user_id], user.name
                )
    except Exception as ex:
        print(f"Error Occured: {ex}")
