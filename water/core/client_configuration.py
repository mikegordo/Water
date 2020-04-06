import json

from water.core.messages.water import WaterMessage
from water.logger import app


class ClientConfiguration:
    """
    Configuration for a clients.
    Describes pots, group and a broker
    """

    def __init__(self, filename):
        self.filename = filename
        self.raw = self.get_raw_configuration(filename)
        self.broker = self.raw['broker']
        self.group = self.raw['group']

    @staticmethod
    def get_raw_configuration(filename):
        try:
            with open(filename, 'r') as outfile:
                return json.load(outfile)
        except Exception as e:
            app.logger.error(e)
            raise

    def match_configuration(self, message: WaterMessage):
        pot_id = message.pot_id
        if not self.raw['pots']:
            return False
        for p in self.raw['pots']:
            if p['id'] == pot_id:
                return p
        return False

    def get_pots(self):
        return self.raw['pots']
