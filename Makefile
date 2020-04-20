.PHONY: default client clean kill build

default:
	docker-compose up -d

build:
	docker-compose up -d --build

clean:
	docker-compose down

kill:
	docker-compose down --rmi all

client:
	# Starting the worker for water topic on Raspberry Pi
ifndef CONFIG
	# CONFIG is required
else
	FLASK_APP=water FLASK_ENV=development flask start_client $(CONFIG)
endif
