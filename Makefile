DC=docker compose

APP=docker/docker-compose.app.yaml
DEV=docker/docker-compose.dev.yaml
DEPLOY=docker/docker-compose.deploy.yaml
ENV_FILE = --env-file ./.env


up-dev:
	$(DC) -f $(APP) -f $(DEV) ${ENV_FILE} up -d --build --abort-on-container-exit --attach app --no-log-prefix

up-deploy:
	$(DC) -f $(APP) -f $(DEPLOY) ${ENV_FILE} up -d --build

down-deploy:
	$(DC) -f $(APP) -f $(DEPLOY) down


