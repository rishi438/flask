///////////////////////////Backend\\\\\\\\\\\\\\\\\\\\\\\
Prerequisites RabbitMQ or RabbitMQ Image in Docker
>>>>>>>>>>>>>setup<<<<<<<<<<<<
----------->Navigate to backend folder and run these<------------
.venv\Scripts\activate
 python.exe -m pip install --upgrade pip
pip install -r requirement.txt

>>>>>>>>>>>>Running<<<<<<<<<<<
<terminal1> python run.py
<terminal2> celery -A run.celery_scheduler worker --pool=solo -l info                 {{Worker}}
<terminal3> celery -A run.celery_scheduler beat -l info                              {{Scheduler}}
<terminal4> celery -A run.celery_scheduler flower                    {{check Job Status GUI}} - {{Not Necessary}}


///////////////////////////Frontend\\\\\\\\\\\\\\\\\\\\\\\\\
Prerequisites Nodejs
>>>>>>>>>>>>>setup<<<<<<<<<<<<
----------->Navigate to frontend folder and run these<------------
npm i {already downloaded modules}
npm run preview


*************************************SAMPLE API****************************************
Expense Add API - http://127.0.0.1:5000/api/add-expense/
body={
    "amount": 6000,
    "payer": "b095f9f4-8208-4f75-92d3-10043d0d12ff",
    "type": "EQUAL",
    "participants": ["83e7d98e-050e-42ee-8bbb-02ddcc8e0ea7", "b095f9f4-8208-4f75-92d3-10043d0d12ff", "2c91b44f-a3c7-4fa5-b005-5f52842b9f4b",
    "33c24a55-3068-4092-a4e0-3a89a0a7b5c9","556145f8-9227-4d00-a277-142ecce45485"],
    "shares": []
}
User addtion API - http://127.0.0 - 5000/api/add/

Balance API - http://127.0.0.1:5000/api/show-balances/83e7d9-050e-42ee-8bbb-02ddcc8e0ea7/
