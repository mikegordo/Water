import traceback
from json import loads

from kafka import KafkaConsumer

from water.core.messages.moisture import MoistureMessage
from water.logger import app
from .abort_exception import AbortException
from .base import Base, DEFAULT_BROKER, DEFAULT_GROUP
from .decider import Decider
from .topics import MOISTURE_TOPIC


class ServerConsumer(Base):
    """
    Collects information about moisture
    Decides if watering is needed
    """

    def __init__(self, db, broker, group):
        # setting the right topic
        self.topic = MOISTURE_TOPIC
        self.force_stop = False
        if db:
            self.db = db
            # making an instance of a decider
            self.decider = Decider(db)
        # group of pots
        self.group = group or DEFAULT_GROUP
        self.broker = broker or DEFAULT_BROKER
        # kafka consumer
        self.c = None

    def start(self):
        """
        Create an instance of kafka consumer
        Listen indefinitely or until force_stop is called
        """
        self.c = KafkaConsumer(
            self.topic,
            bootstrap_servers=[self.broker],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=self.group,
            value_deserializer=lambda x: loads(x.decode('utf-8')))

        for message in self.c:
            if self.force_stop:
                break
            message = message.value
            app.logger.info('Received message: {}'.format(message))
            self.process_message(message)
        self.c.close()

    def process_message(self, message):
        """
        Processing message received by kafka consumer
        (storing moisture data and deciding if watering required)
        """
        try:
            message = MoistureMessage(message)
            self.ignore_control_message(message)
            self.save_moisture_to_db(message)
            self.decider.decide(message)
        except AbortException:
            pass
        except Exception as e:
            app.logger.error("Error while processing message {}: {} {}".format(message, e, traceback.format_exc()))

    def save_moisture_to_db(self, message):
        """
        Storing moisture information to db
        """
        self.db.execute(
            'INSERT INTO "moisture" (pot_id, value, description) '
            'VALUES (?, ?, ?)',
            (message.pot_id, message.value, message.description)
        )
        self.db.commit()
