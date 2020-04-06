import json
import traceback

import gpiozero
from time import sleep

from water.core.messages.water import WaterMessage
from water.logger import app
from .abort_exception import AbortException
from .client_configuration import ClientConfiguration
from .server_consumer import ServerConsumer
from .skip_exception import SkipException
from .topics import WATER_TOPIC


class ClientConsumer(ServerConsumer):
    """
    Receiving message to start watering a plant
    """

    def __init__(self, configuration: ClientConfiguration):
        super().__init__(db=None, broker=configuration.broker, group=configuration.group)
        self.topic = WATER_TOPIC
        self.configuration = configuration
        self.pumps = {}

    def process_message(self, message) -> None:
        """
        Processing message from the server
        """
        try:
            message = WaterMessage(message)
            self.match_destination(message)
            self.detect_control_message(message)
            self.execute_action(message)
        except SkipException:
            pass
        except AbortException:
            app.logger.info('received command {}'.format(message.command))
            setattr(self, message.command, True)
        except Exception as e:
            app.logger.error("Error while processing message {}: {} {}".format(message, e, traceback.format_exc()))

    def match_destination(self, message: WaterMessage) -> None:
        """
        Determines if message came to the right destination
        """
        if not self.configuration.match_configuration(message):
            raise SkipException

    def execute_action(self, message: WaterMessage) -> None:
        """
        Executing command
        """
        x = self.configuration.match_configuration(message)  # local pot configuration
        watering_command = x  # dict {"id": 1, "configuration": {"pin": 21}}
        watering_command.update(message.get_dict())  # watering message
        self.start_watering_plant(watering_command)

    def start_watering_plant(self, watering_command) -> None:
        """
        Start watering plant - GPIO
        """
        pin = watering_command['pump_pin']
        pump = self.get_pump_by_pin(pin)
        if not pump:
            raise Exception(f'Pump with pin {pin} cannot be accessed.')

        try:
            app.logger.info('Watering command {}'.format(json.dumps(watering_command)))
            pump.on()
            sleep(watering_command['value'])
        except:
            raise
        finally:
            pump.off()

    def get_pump_by_pin(self, pin):
        """
        Return a device (create first if not exists)
        """
        if not self.pumps.get(f'{pin}', False):
            self.pumps[f'{pin}'] = gpiozero.DigitalOutputDevice(pin, active_high=False)
        return self.pumps[f'{pin}']
