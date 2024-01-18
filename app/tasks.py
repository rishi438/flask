# from celery import shared_task
from flask_mail import Message
from app_build import create_app
from celery.schedules import crontab

app, mail, celery_task = create_app()

celery_task.conf.beat_schedule = {
    'send-weekly-balance-notification': {
        'task': 'celery_task.task.send_weekly_balance_notification',
        'schedule': crontab(day_of_week=4, hour=16, minute=32),
    },
}

@celery_task.task
def send_expense_notification(email, expense_amount,paid_by):
    try:
        msg = Message(
            subject='Expense Notification',
            recipients=[email],
            body=f'You have been added to an expense. Total amount you owe: Rs. {expense_amount} to {paid_by}'
        )
        mail.send(msg)
    except Exception as ex:
        print(f"Error Occured: {ex}")

@celery_task.task
def send_weekly_balance_notification(email, total_owe_amount):
    try:
        msg = Message(
            subject='Weekly Balance Notification',
            recipients=[email],
            body=f'Weekly summary: You owe a total of Rs. {total_owe_amount} to other users.'
        )
        mail.send(msg)
    except Exception as ex:
        print(f"Error Occured: {ex}")
