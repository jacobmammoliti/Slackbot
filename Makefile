REPOSITORY_NAME=jacobmammoliti/slackbot
VERSION=1.0
IMAGE_TAG=$(REPOSITORY_NAME):$(VERSION)

docker-build:
	docker build --tag $(IMAGE_TAG) \
	--tag $(REPOSITORY_NAME):latest .