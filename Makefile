SHELL := /bin/bash

manage_py := python ./manage.py

# build:
# 	docker-compose down && docker-compose up -d

runserver:
	$(manage_py) runserver

makemigrations:
	$(manage_py) makemigrations

worker:
	cd app && celery -A settings worker -l debug

beat:
	cd app && celery -A settings beat -l info

migrate:
	$(manage_py) migrate

generate_data:
	$(manage_py) generate_data

parse:
	$(manage_py) parse_pb

createsuperuser:
	$(manage_py) createsuperuser

show_urls:
	$(manage_py) show_urls

shell:
	$(manage_py) shell_plus --print-sql

pytest:
	pytest app/tests/ --cov=app --cov-report html && coverage report --fail-under=71.3910

# gunicorn:
# 	cd app && gunicorn -w 4 settings.wsgi:application -b 0.0.0.0:8001 --log-level=DEBUG

wsgi:
	uwsgi --http :8001 --module currency.wsgi

show-coverage:  ## open coverage HTML report in default browser
	python3 -c "import webbrowser; webbrowser.open('.pytest_cache/coverage/index.html')"

# services:
# 	docker run -d -p 11211:11211 memcached && docker run -d -p 5672:5672 rabbitmq:3.8