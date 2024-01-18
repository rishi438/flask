# from celery import shared_task
from flask_mail import Message
from app_build import create_app

app, mail, celery = create_app()

@celery.task
def send_expense_notification(email, expense_amount,paid_by):
    with app.app_context():
        try:
            msg = Message(
                subject='Expense Notification',
                recipients=[email],
                body=f'You have been added to an expense. Total amount you owe: Rs. {expense_amount} to {paid_by}'
            )
            mail.send(msg)
        except Exception as ex:
            print(f"Error Occured: {ex}")

@celery.task
def send_weekly_balance_notification(email, total_owe_amount):
    msg = Message(
        subject='Weekly Balance Notification',
        recipients=[email],
        body=f'Weekly summary: You owe a total of Rs. {total_owe_amount} to other users.'
    )
    mail.send(msg)
