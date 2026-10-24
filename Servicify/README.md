# Servicify

Django app for booking home services in Dhaka.

## Run
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```
Demo logins (password `demo1234`): customers `rahim`, `nadia`; providers e.g. `karim_plumber`.
