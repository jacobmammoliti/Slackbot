REPOSITORY_NAME=jacobmammoliti/slackbot
VERSION=0.2
IMAGE_TAG=$(REPOSITORY_NAME):$(VERSION)

docker: docker-build docker-publish

docker-build:
	docker build -t $(IMAGE_TAG) \
	-t $(REPOSITORY_NAME):latest . 

docker-publish:
	docker push $(IMAGE_TAG)
	docker push $(REPOSITORY_NAME):latest

docker-multiarch-build-publish:
	docker buildx build \
	--push \
	--tag $(IMAGE_TAG) \
	--tag $(REPOSITORY_NAME):latest \
	--platform linux/amd64,linux/arm64 \
	--file Dockerfile .