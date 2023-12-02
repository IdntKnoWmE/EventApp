# Instruction to the Project event_service

## Built with
- [Python 3.11](https://docs.python.org/3.11/)
- [PostgreSQL](https://www.postgresql.org/)
- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)


## Running locally

1. Create an Virtual Env.
2. In that, virtual env installs python 3.11 version.
3. Then copy-paste the project in the virtual env.
4. Now, using **`ls`** and **`cd`** move to the folder in which manage.py file is present.
5. Run, `pip install -r requirements.txt` to install the modules and libraries.
6. Then copy and paste this in settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': your_postgres_db_name,
        'USER': yours_postgres_user,
        'PASSWORD': yours_postgres_password,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
Please create a postgres database in your system and fill out the required details and then copy-paste the above details.

7. Run `python manage.py make migrate to create the tables in the database.`
8. To populate raw data please run management command `python manage.py initial_setup`.
9. Now, with the use of postman's collection in the project, please run the API to verify the features in the event app.


## Features of APP
1. User registration.
2. User login and logout.
3. Event creation.
4. Event rate.
5. Show Interest in the event.
6. Get the list of events with average rating, average rating given by members living in
the same city where the event is happening(city_member_rating) and count of the users
interested in the event.