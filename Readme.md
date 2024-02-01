# Backend

## Prerequisites
- RabbitMQ or RabbitMQ Image in Docker

## Setup
1. Navigate to the `backend` folder.
2. Activate the virtual environment: `.venv\Scripts\activate`
3. Upgrade pip: `python.exe -m pip install --upgrade pip`
4. Install dependencies: `pip install -r requirement.txt`
5. Configure Gmail SMTP with Password,Mail and Username 

## Running
- Run RabbitMQ service
- **Terminal 1:** `python run.py`
- **Terminal 2:** `celery -A run.celery_scheduler worker --pool=solo -l info` (Worker)
- **Terminal 3:** `celery -A run.celery_scheduler beat -l info` (Scheduler)
- **Terminal 4:** `celery -A run.celery_scheduler flower` (Check Job Status GUI, Not Necessary)
#### OR
### Automated running
***Run directly start_app.exe***  

# Frontend

## Prerequisites
- Node.js

## Setup
1. Navigate to the `frontend` folder.
2. Install dependencies: `npm install`

## Running
- **Terminal:** `npm run preview`

# Sample API

### Expense Add API
- **Endpoint:** `http://127.0.0.1:5000/api/add-expense/`
- **Body:**
  ```json
  {
      "amount": 6000,
      "payer": "b095f9f4-8208-4f75-92d3-10043d0d12ff",
      "type": "EQUAL",
      "participants": [
          "83e7d98e-050e-42ee-8bbb-02ddcc8e0ea7",
          "b095f9f4-8208-4f75-92d3-10043d0d12ff",
          "2c91b44f-a3c7-4fa5-b005-5f52842b9f4b",
          "33c24a55-3068-4092-a4e0-3a89a0a7b5c9",
          "556145f8-9227-4d00-a277-142ecce45485"
      ],
      "shares": []
  }
**User addtion API** - ```http://127.0.0.1:5000/api/add/```

**Balance API** - ```http://127.0.0.1:5000/api/show-balances/83e7d9-050e-42ee-8bbb-02ddcc8e0ea7/```
