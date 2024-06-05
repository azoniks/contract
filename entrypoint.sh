python manage.py makemigrations --no-input

python manage.py migrate --no-input

python manage.py collectstatic --no-input

exec gunicorn contracts.wsgi:application --bind 0.0.0.0:$PORT --reload
