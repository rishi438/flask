from flask import request,jsonify,Blueprint
from app.models import Balance, Expense,db,User
from app.tasks import send_expense_notification

api_routes=Blueprint("api",__name__)

@api_routes.route("/add/",methods=["POST"])
def add_user():
    try:    
        data=request.get_json() or {}
        user = User(
            name=data.get('name'),
            email= data.get('email'),
            phone_number=data.get('phone_number')
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(response={"msg":"added successfully"})
    except Exception as ex:
        print(f"Error Adding User: {ex}")
        return jsonify({'error': 'Failed to add user'})


# @api_routes.route('/add_expense/', methods=['POST'])
# def add_expense():
#     try:
#         data = request.get_json()
#         amount = float(data.get('amount'))
#         payer_id = data.get('payer_id')
#         participant_ids = data.get('participants')
#         payer = User.query.get(payer_id)
#         participants = User.query.filter(User.user_id.in_(participant_ids)).all()
#         expense = Expense(amount=amount, payer=payer, participants=participants)
#         db.session.add(expense)
#         db.session.flush()
#         for participant in participants:
#             if participant.user_id != payer_id:
#                 balance = Balance(creditor_id=payer_id, debitor_id=participant.user_id, amount=round(amount / len(participants),2))
#                 db.session.add(balance)
#         db.session.commit()
#         return jsonify({'message': 'Expense added successfully'})
#     except Exception as ex:
#         db.session.rollback()
#         print(f"Error adding expense: {ex}")
#         return jsonify({'error': 'Failed to add expense'})

    
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
        result=calculate_expense(expense)
        if result:
            return jsonify({"message": "Expense added successfully"})
        else:
            return jsonify({"message": "Error Occured Contact Tech Team"})
    except Exception as e:
        return jsonify({"error": str(e)})


@api_routes.route("/show-balances/<user_id>/", methods=["GET"])
def show_balances(user_id):
    balances = Balance.query.filter((Balance.creditor_id == user_id) | (Balance.debitor_id == user_id)).all()
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
        participants = User.query.filter(User.user_id.in_(payload.get("participants"))).all()
        total_participants = len(participants)
        amount = payload.get("amount")
        user_amount={}
        if payload.get("type") == "EQUAL":
            for participant in participants:
                shared_amount=round(amount / total_participants,2)
                balance = Balance(
                    creditor_id=payload.get("payer"),
                    debitor_id=participant.user_id,
                    amount=shared_amount,
                )
                db.session.add(balance)
                user_amount[participant.user_id]=shared_amount
        elif payload.get("type") == "EXACT":
            for share in payload.get("shares"):
                debitor_id = share.get("user_id")
                shared_amount = round(share.get("amount"),2)
                balance = Balance(creditor_id=payload.get("payer"), debitor_id=debitor_id, amount=shared_amount)
                db.session.add(balance)
                user_amount[debitor_id]=shared_amount
        elif payload.get("type") == "PERCENT":
            total_percent = sum(share.get("percent") for share in payload.get("shares"))
            if total_percent != 100:
                raise print("Total percentage shares must equal 100.")
            for share in payload.get("shares"):
                debitor_id = share.get("user_id")
                shared_amount=round(((amount * share.get("percent")) / 100),2)
                balance = Balance(creditor_id=payload.get("payer"), debitor_id=debitor_id, amount=shared_amount)
                db.session.add(balance)
                user_amount[debitor_id]=shared_amount
        expense = Expense(
            amount=payload.get("amount"),
            payer_id=payload.get("payer"),
            expense_type=payload.get("type"),
        )
        db.session.add(expense)
        for participant in participants:
            simplify_balances(participant.user_id)
        db.session.commit()
        expense_notification_sender(participants,user_amount,payload.get("payer"))
        return True
    except Exception as ex:
        print(f"Error occured: {ex}")
        return False
        

def simplify_balances(user_id):
    balances = Balance.query.filter((Balance.creditor_id == user_id) | (Balance.debitor_id == user_id)).all()
    user = User.query.get(user_id)
    user.balance=0
    for balance in balances:
        if  balance.creditor_id != balance.debitor_id:
            if balance.creditor_id==user_id:
                user.balance+=balance.amount
            elif balance.debitor_id==user_id:
                user.balance-=balance.amount
    db.session.flush()
    
    # balances = Balance.query.filter((Balance.creditor_id == user_id) | (Balance.debtor_id == user_id)).all()

    # # Initialize a dictionary to store balances for each user
    # user_balances = {}

    # for balance in balances:
    #     creditor_id = balance.creditor_id
    #     debtor_id = balance.debtor_id
    #     amount = balance.amount

    #     # Update the balance for the creditor
    #     if creditor_id == user_id:
    #         user_balances[debtor_id] = user_balances.get(debtor_id, 0) - amount
    #     # Update the balance for the debtor
    #     else:
    #         user_balances[creditor_id] = user_balances.get(creditor_id, 0) + amount
        
    #     for user, balance in user_balances.items():
    #         print(f"User {user} owes {user_id} ${abs(balance):.2f}")
    
def expense_notification_sender(participants,user_amount,payer_id):
    try:
        user = User.query.get(payer_id)
        for participant in participants:
            if participant.user_id in user_amount:
                send_expense_notification.delay(participant.email, user_amount[participant.user_id], user.name)
    except Exception as ex:
        print(f"Error Occured: {ex}")
    