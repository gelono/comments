release: python manage.py migrate
web: gunicorn --bind 0.0.0.0:$PORT comments_project.app
