import copy
from json import dumps

from kafka import KafkaProducer

from water.core.messages.message import Message
from water.logger import app
from .base import DEFAULT_BROKER


class DMSProducer:
    """
    Distributed Messaging System producer
    """

    def __init__(self, broker=None):
        self.broker = broker or DEFAULT_BROKER
        self.p = KafkaProducer(bootstrap_servers=[self.broker],
                               value_serializer=lambda x: dumps(x).encode('utf-8'))

    def submit(self, topic, message_):
        """
        Submits the message to the topic
        """
        message = copy.copy(message_)
        if isinstance(message, Message):
            message = message.get_message(is_dict=True)

        try:
            self.p.send(topic, value=message)
        except Exception as e:
            app.logger.error('Message send failed: {}'.format(e))

    def close(self, timeout=3):
        self.p.close(timeout=timeout)
