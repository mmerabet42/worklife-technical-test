.ONESHELL:

# used in order to fetch the proper .env file, by default it is empty so it uses app.env
# env must be equal to whatever is in place the wildcard: app.*.env
# for the test environment for example, you would set it to 'test'
ENV = dev
ENV_FILE = app$(if $(ENV),.$(ENV)).env
WITH_ENV = env `grep -v '^\#' $(ENV_FILE)`

COMPOSER = docker compose -f ./docker-compose.yml
CONTAINER_EXECUTOR = docker exec -w /wl/app worklife-test-api
DATABASE_EXECUTOR = docker exec worklife-test-db

# Deployment
.PHONY: up
up:
	$(COMPOSER) up -d

.PHONY: up
reup:
	$(COMPOSER) up -d --build

.PHONY: down
down:
	$(COMPOSER) down -v

.PHONY: logs
logs:
	$(COMPOSER) logs --follow

.PHONY: test
test:
	$(CONTAINER_EXECUTOR) poetry run $(WITH_ENV) pytest -rP

.PHONY: build
build:
	$(COMPOSER) build

# DB
.PHONY: create-db
create-db:
	$(DATABASE_EXECUTOR) psql -U dev -d postgres -f /scripts/create_db.sql -v db=$(ENV)

.PHONY: downgrade-db
downgrade-db:
	$(CONTAINER_EXECUTOR) $(WITH_ENV) alembic downgrade -1

.PHONY: migrate-db
migrate-db:
	$(CONTAINER_EXECUTOR) $(WITH_ENV) alembic upgrade head

.PHONY: autogenerate-migration
autogenerate-migration:
	$(CONTAINER_EXECUTOR) $(WITH_ENV) alembic revision --autogenerate -m $(revision_message)