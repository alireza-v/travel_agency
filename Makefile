help:
	@echo "Available commands:"
	@echo "  make run       - Start the development server on port 7001"
	@echo "  make db        - Apply database migrations"
	@echo "  make shell     - Open the Django shell"
	@echo "  make clean     - Format code using isort and ruff"
	@echo "  make admin     - Create a superuser account"


run:
	python manage.py runserver 7001

db:
	python manage.py makemigrations
	python manage.py migrate

shell:
	python manage.py shell

clean:
	isort .
	ruff format

admin:
	python manage.py createsuperuser