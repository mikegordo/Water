.PHONY: default server test kafka kafka-shell consumer pi consumer_pi server_kafka server_zookeeper

default:
	# Not Defined

kafka:
	# organize repository, spin up images for kafka and zookeeper
	git clone https://github.com/wurstmeister/kafka-docker.git
	docker-compose up -d

kafka-shell:
	# Starting Kafka shell

	# To display topics run
	# $KAFKA_HOME/bin/kafka-topics.sh --list --bootstrap-server kafka:9092

	# To create a new topic run
	# $KAFKA_HOME/bin/kafka-topics.sh --create --partitions 1 --bootstrap-server kafka:9092 --topic test

	# To create a consumer
	# $KAFKA_HOME/bin/kafka-console-consumer.sh --from-beginning --bootstrap-server kafka:9092 --topic=test

	# To create a producer
	# $KAFKA_HOME/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic=test
	docker exec -i -t -u root $$(docker ps | grep water_kafka | cut -d' ' -f1) /bin/bash

server:
	# Starting the application
	FLASK_APP=water FLASK_ENV=development flask run --host=0.0.0.0

consumer:
	# Starting the consumer for moisture topic
	FLASK_APP=water FLASK_ENV=development flask start_server_consumer

client:
	# Starting the worker for water topic on Raspberry Pi
ifndef CONFIG
	# CONFIG is required
else
	FLASK_APP=water FLASK_ENV=development flask start_client $(CONFIG)
endif

test:
	FLASK_APP=water FLASK_ENV=development pytest

server_zookeeper:
	cd /home/himor/Downloads/kafka_2.12-2.4.0 && ./bin/zookeeper-server-start.sh config/zookeeper.properties

server_kafka:
	cd /home/himor/Downloads/kafka_2.12-2.4.0 && ./bin/kafka-server-start.sh config/server.properties

