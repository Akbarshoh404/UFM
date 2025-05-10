release: . /opt/venv/bin/activate && flask db migrate && flask db upgrade
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app