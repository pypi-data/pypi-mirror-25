image := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
tag := $(shell date -I'date'| tr -d "[:punct:]")

start:
	systemctl start docker

build:
	docker build -f $(image).Dockerfile -t fluiddyn/$(image) .
	docker tag fluiddyn/$(image) fluiddyn/$(image):$(tag)

build_nocache:
	docker build -f $(image).Dockerfile -t fluiddyn/$(image) . --no-cache
	docker tag fluiddyn/$(image) fluiddyn/$(image):$(tag)

onbuild:
	docker build -f $(image).onbuild.Dockerfile -t fluiddyn/$(image):onbuild .

push:
	docker push fluiddyn/$(image)

run:
	docker run -it fluiddyn/$(image) bash

run_travis:
	docker run -it travisci/ci-python bash -c "su - travis"

run_travis_old:
	docker run -it quay.io/travisci/travis-python bash -c "su - travis"
