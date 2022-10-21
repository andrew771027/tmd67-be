format:
	autoflake -ir --remove-all-unused-imports .
	isort .
	black .

lint:
	flake8

mypy:
	mypy .

migrate:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py loaddata data.json

run:
	sudo -E uwsgi --ini uwsgi.ini
