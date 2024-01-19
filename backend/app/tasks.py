from smtplib import SMTPException

from celery.schedules import crontab
from flask_mail import Message
from sqlalchemy.exc import SQLAlchemyError

from app_build import create_app
from app.models import Balance, User

app, mail, celery_task = create_app()


def init_celery(app, celery):
    celery.conf.beat_schedule = {
        "send-weekly-balance-notification": {
            "task": "app.tasks.send_weekly_balance_notification",
            "schedule": crontab(day_of_week=3, hour=10, minute=13),
        },
    }
    celery.conf.enable_utc = False
    celery.conf.timezone = "Asia/Kolkata"
    return celery


@celery_task.task
def send_expense_notification(email, expense_amount, paid_by):
    with app.app_context():
        try:
            msg = Message(
                subject="Expense Notification",
                recipients=[email],
                body=f"""You have been added to an expense.
                Total amount you owe: Rs. {expense_amount} to {paid_by}""",
            )
            mail.send(msg)
        except SQLAlchemyError as db_error:
            print(f"Database Error: {db_error}")
        except SMTPException as smtp_error:
            print(f"SMTP Error: {smtp_error}")


@celery_task.task
def send_weekly_balance_notification():
    with app.app_context():
        try:
            users = User.query.all()
            for user in users:
                body = weekly_mail_body(user.user_id, user.name)
                weekly_email(user.email, body)
        except SQLAlchemyError as db_error:
            print(f"Database Error: {db_error}")
        except SMTPException as smtp_error:
            print(f"SMTP Error: {smtp_error}")


def weekly_mail_body(user_id, user_name):
    balances = Balance.query.filter(
        (Balance.creditor_id == user_id) | (Balance.debitor_id == user_id)
    ).all()
    user_balances = {}

    for balance in balances:
        creditor_id = balance.creditor_id
        debitor_id = balance.debitor_id
        amount = balance.amount
        if creditor_id == user_id:
            user_balances[debitor_id] = user_balances.get(
                debitor_id, {"amount": 0, "name": balance.debitor.name}
            )
            user_balances[debitor_id]["amount"] -= amount
        else:
            user_balances[creditor_id] = user_balances.get(
                creditor_id, {"amount": 0, "name": balance.creditor.name}
            )
            user_balances[creditor_id]["amount"] += amount

    body = ""
    for user, balance_info in user_balances.items():
        body += f"""User {balance_info['name']} owes
        {user_name} {abs(balance_info['amount']):.2f}\n"""

    return body


def weekly_email(email, body):
    try:
        msg = Message(
            subject="Weekly Balance Notification",
            recipients=[email],
            body=body
        )
        mail.send(msg)
    except SMTPException as ex:
        print(f"SMTP Error Occurred: {ex}")
