
RM-SDK := rm-sdk:latest

docker-build:
	docker build -t $(RM-SDK) .
