## IS5009 Final Project - Procurement Economies of Scale (PEOS)

PEOS is a Web Application for SME Buyers and Suppliers.

### Requirements:
```
* PostgreSQL >= 9.4
* Python >= 3.6
* pip install -r requirements.txt
```

### Detailed Setup Instructions:
**Step 1: Clone this repo to the desired location.**


**Step 2: Install PostgreSQL** 
1. Download at https://www.postgresql.org/download/
2. Downloaded version must be 9.4 or greater.


**Step 3: Run SQL Shell**

In SQL Shell, use the following steps to setup DB:
```
1. CREATE USER is5009 WITH PASSWORD 'is5009pw123';
2. CREATE DATABASE peos_db;
3. ALTER ROLE is5009 SET client_encoding TO 'utf8';
4. ALTER ROLE is5009 SET default_transaction_isolation TO 'read committed';
5. ALTER ROLE is5009 SET timezone TO 'UTC';
6. GRANT ALL PRIVILEGES ON DATABASE PEOS_DB TO is5009;
7. ALTER USER is5009 CREATEDB;
```

**Step 4: Run CMD/Terminal**.

Step to create Django user:
```
python manage.py createsuperuser --username=is5009 --email=is5009@gmail.com
```

Server Setup:
```
1. pip install -r requirements.txt
2. python manage.py makemigrations
3. python manage.py migrate
4. python manage.py runserver 
```

Once all the above steps are completed, go to **localhost:8000** on your browser to use our application!
