import traceback
from typing import Union

import gpiozero
from time import sleep

from water.core.client_configuration import ClientConfiguration
from water.core.messages.moisture import MoistureMessage
from water.core.producer import DMSProducer
from water.core.topics import MOISTURE_TOPIC
from water.logger import app

INTERVAL = 60  # seconds


class Client:
    """
    Client is process that runs indefinitely
    It measures the moisture and submits information to kafka topic
    """

    def __init__(self, configuration: ClientConfiguration):
        self.producer = DMSProducer(broker=configuration.broker)
        self.configuration = configuration
        self.sensors = {}

    def start(self) -> None:
        """
        Every INTERVAL seconds submit information about pot's moisture to kafka topic
        """
        while True:
            sleep(INTERVAL)
            for pot in self.configuration.get_pots():
                moisture_message = self.build_message(pot)
                if moisture_message:
                    self.producer.submit(MOISTURE_TOPIC, moisture_message)
                    app.logger.info('Moisture sensor pot ID: {}, value: {}'.format(moisture_message.pot_id,
                                                                                   moisture_message.value))

    def build_message(self, pot_configuration) -> Union[MoistureMessage, None]:
        try:
            message = MoistureMessage({'pot_id': pot_configuration['id'],
                                       'value': self.get_moisture_value(pot_configuration),
                                       'description': 'Moisture sensor value'})
            return message
        except Exception as e:
            app.logger.error("Error building moisture message: {} {}".format(e, traceback.format_exc()))
            return None

    def get_moisture_value(self, pot_configuration) -> float:
        """
        Get sensor value, return float
        Can throw an exception
        """
        channel = pot_configuration['sensor_pin']
        sensor = self.get_sensor_by_pin(channel)
        return 100.0 * sensor.value

    def get_sensor_by_pin(self, channel):
        """
        Return a device (create first if not exists)
        """
        if not self.sensors.get(f'{channel}', False):
            self.sensors[f'{channel}'] = gpiozero.MCP3008(channel=channel)
        return self.sensors[f'{channel}']
