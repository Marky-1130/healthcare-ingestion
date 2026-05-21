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

start:
	cp .env.example .env || true
	docker compose up--build-d
	sleep 10
	docker exec healthcare-localstack awslocal s3 mb s3://patient-intake || true
	@echo "System started successfully"