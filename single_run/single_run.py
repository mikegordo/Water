"""
In case of a dedicated server not being an option
this file can be used instead of everything else.
"""
import json
from datetime import timedelta, datetime

import gpiozero
from time import sleep

last_water_counter = {}
pumps = {}
sensors = {}

DELAY = 60
WATER_INTERVAL = 3600


def main():
    configuration = load_configuration()
    pots = configuration['pots']
    while True:
        for pot in pots:
            if should_water(pot):
                do_water(pot)
        sleep(DELAY)


def load_configuration():
    try:
        with open('configuration.json', 'r') as outfile:
            return json.load(outfile)
    except Exception as e:
        say(e)
        raise


def should_water(pot):
    if pot['id'] not in last_water_counter:
        last_water_counter[pot['id']] = datetime.now() - timedelta(seconds=WATER_INTERVAL)
    elif last_water_counter[pot['id']] + timedelta(seconds=WATER_INTERVAL) > datetime.now():
        return False
    return read_sensor(pot) < pot['sensor_threshold']


def do_water(pot):
    if pot['id'] not in pumps:
        pumps[pot['id']] = gpiozero.DigitalOutputDevice(pot['pump_pin'], active_high=False)

    try:
        say('Watering pot {}'.format(pot['id']))
        pumps[pot['id']].on()
        sleep(pot['duration'])
    except Exception as e:
        say('Failed: {}'.format(str(e)))
    finally:
        pumps[pot['id']].off()


def read_sensor(pot):
    if pot['id'] not in sensors:
        sensors[pot['id']] = gpiozero.MCP3008(pot['sensor_pin'])
    return 100.0 * sensors[pot['id']].value


def say(e):
    print(str(e))


if __name__ == '__main__':
    main()
