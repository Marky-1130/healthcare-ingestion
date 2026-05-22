build:
	docker compose build

up:
	docker compose up-d

down:
	docker compose down

logs:
	docker compose logs-f

create-bucket:
	docker exec healthcare-localstack awslocal s3 mb s3://patient-intake

migrate:
	docker compose exec api alembic upgrade head

makemigration:
	docker compose exec api alembic revision --autogenerate -m "$(msg)"

rollback:
	docker compose exec api alembic downgrade-1

start:
	cp .env.example .env || true
	docker compose up --build -d
	sleep 10
	docker exec healthcare-localstack awslocal s3 mb s3://patient-intake || true
	docker compose exec api alembic upgrade head
	@echo "System started successfully"