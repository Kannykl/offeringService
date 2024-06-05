.PHONY: build drun stop run

build:
	docker build . -t offer_service
drun:
	docker run -p ${SERVER_PORT}:8000 --rm -d --name offer_service offer_service
stop:
	docker stop offer_service

run:
	python -m offer

test:
	pytest -v
