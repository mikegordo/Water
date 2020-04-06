from datetime import datetime, timedelta

import pytz

from water.core.messages.moisture import MoistureMessage
from water.core.messages.water import WaterMessage
from water.core.producer import DMSProducer
from water.core.topics import WATER_TOPIC
from water.logger import app


class Decider:
    """
    Decides if watering is needed
    Produces watering message if required
    """

    # water plants maximum once every DELAY seconds
    DELAY = 3600  # one hour

    def __init__(self, db):
        self.pots = None
        self.db = db
        self.load_pots()
        self.producer = None

    def load_pots(self):
        """
        Loading all pots into a class property
        """
        pots = self.db.execute(
            'SELECT * FROM pot p ORDER BY p.id'
        ).fetchall()
        self.pots = {}
        for p in pots:
            self.pots[p['id']] = p

    def load_watering(self, pot_id) -> dict:
        """
        Get a watering history of the pot
        """
        # refresh pots, make sure it's a valid one
        self.load_pots()
        if pot_id not in self.pots:
            app.logger.warning('Unknown pot id {}.'.format(pot_id))
            return {}

        # load all watering of this pot in last 2 weeks, latest first
        last_week = datetime.today() - timedelta(days=14)
        watering = self.db.execute(
            'SELECT * FROM water w WHERE created > ? AND w.pot_id = ? ORDER BY w.created DESC LIMIT 10',
            (last_week, pot_id)
        ).fetchall()
        w = self.get_watering_for_pot(watering)
        last_water = w[0]['created'] if len(w) else None
        result = {'id': pot_id,
                  'name': self.pots[pot_id]['name'],
                  'description': self.pots[pot_id]['description'],
                  'water_value': self.pots[pot_id]['water_value'],
                  'moisture_value': self.pots[pot_id]['moisture_value'],
                  'last_water': last_water
                  }
        return result

    @staticmethod
    def get_watering_for_pot(watering) -> list:
        """
        Organize given watering
        """
        result = []
        for m in watering:
            result.append({'id': m['id'],
                           'value': m['value'],
                           'description': m['description'],
                           'created': m['created'],
                           })
        return result

    def decide(self, message: MoistureMessage) -> bool:
        """
        Decide if watering is required based on a moisture message
        """
        watering = self.load_watering(message.pot_id)
        if not watering:
            return False
        if watering['moisture_value'] < message.value:
            app.logger.info('Pot [{}] {} current moisture {} more than {}.'.format(watering['id'],
                                                                                   watering['name'],
                                                                                   message.value,
                                                                                   watering['moisture_value']))
            return False

        if watering['last_water']:
            when = pytz.timezone('UTC').localize(watering['last_water']) + timedelta(seconds=self.DELAY)
            now = pytz.timezone('UTC').localize(datetime.utcnow())
            if when > now:
                app.logger.info('Pot [{}] {} watered less than {} seconds ago.'.format(watering['id'],
                                                                                       watering['name'],
                                                                                       self.DELAY))
                return False

        app.logger.info('Pot [{}] {} watering required.'.format(watering['id'],
                                                                watering['name']))

        if not self.producer:
            self.producer = DMSProducer()

        # build a message and submit it to a topic
        water_message = WaterMessage({'pot_id': watering['id'],
                                      'value': watering['water_value'],
                                      'created': str(datetime.now()),
                                      'description': 'Watering {}, moisture value {}'.format(watering['name'],
                                                                                             message.value)})
        self.producer.submit(WATER_TOPIC, water_message)

        # store watering information
        self.db.execute(
            'INSERT INTO "water" (pot_id, value, description) '
            'VALUES (?, ?, ?)',
            (water_message.pot_id, water_message.value, water_message.description)
        )
        self.db.commit()

        return True
