up:
	docker compose up

build:
	docker compose build

admin:
	docker compose run backend python manage.py createsuperuser

migrations:
	docker compose run backend python manage.py makemigrations

test:
	docker compose run backend python manage.py test