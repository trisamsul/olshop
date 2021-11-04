## Requirements
- Python 3.0 and above

## Setup
1. Open Console
1. Go to project directory
1. Create virtual environment `python -m venv venv`
1. Activate the virtual environment. 
   - Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate` 
1. Install requirements `pip install -r requirements`
1. Create a new database on localhost named `olshop`
1. Create migrations `python manage.py makemigrations`
1. Run migrations `python manage.py migrate`
1. Seed data `python manage.py loaddata app/seeds/master-data.json`
1. Run service `python manage.py runserver`

When it's okay this message will be shown on the console
```
System check identified no issues (0 silenced).
November 04, 2021 - 19:59:29
Django version 3.2.9, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## Database
Open this link: https://dbdiagram.io/d/61838302d5d522682df807d3

## API Documentation
- Swagger: http://127.0.0.1:8000/swagger
- Postman (Including Login): olshop.postman_collection.json
