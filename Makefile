up:
	docker-compose up
stop:
	docker-compose stop
down:
	docker-compose down
restart:
	docker-compose restart
migrations:
	docker exec -it imagger_django poetry run python3 manage.py makemigrations
migrate:
	docker exec -it imagger_django poetry run python3 manage.py migrate
shell:
	docker exec -it imagger_django poetry run python3 manage.py shell
collectstatic:
	docker exec -it imagger_django poetry run python3 manage.py collectstatic
tests:
	docker exec -it imagger_django poetry run python3 manage.py test