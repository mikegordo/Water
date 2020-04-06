from datetime import datetime, timedelta

import pytz
from flask import (
    request, jsonify
)

from water.auth import login_required, is_valid_authorization_string
from water.core.client import INTERVAL
from water.core.messages.message import Message
from water.core.messages.water import WaterMessage
from water.core.producer import DMSProducer
from water.core.topics import MOISTURE_TOPIC, WATER_TOPIC
from water.db import get_db
from water.views.blueprint import bp

DEFAULT_TIMEZONE = "America/New_York"


@bp.route('/api', methods=('GET', 'POST'))
@login_required
def api_index():
    db = get_db()

    last_moisture = db.execute(
        'SELECT * FROM moisture m GROUP BY pot_id ORDER BY m.created DESC'
    ).fetchall()

    bylast = {}
    for l in last_moisture:
        bylast[l['pot_id']] = l

    pots = db.execute(
        'SELECT * FROM pot p ORDER BY p.id'
    ).fetchall()

    before = datetime.today() - timedelta(hours = 24 * 3)

    moisture = db.execute(
        "SELECT * FROM moisture m WHERE created > ? GROUP BY strftime('%d%H', m.created), pot_id ORDER BY m.created ASC",
        (before,)
    ).fetchall()

    watering = db.execute(
        'SELECT * FROM water w WHERE created > ? ORDER BY w.created DESC LIMIT ?',
        (before, len(pots) * 5)
    ).fetchall()

    return serialized(pots, bylast, moisture, watering)


def serialized(pots, last_, moisture_, watering_):
    result = []
    for p in pots:
        moisture = last_[p['id']]['value'] if p['id'] in last_ else 0
        last_moisture = last_[p['id']]['created'] if p['id'] in last_ else None
        if last_moisture:
            dt = pytz.timezone('UTC').localize(last_moisture)
            last_moisture = dt.astimezone(pytz.timezone(DEFAULT_TIMEZONE))
        moistures = get_moisture_for_pot(moisture_, p['id'])
        double_interval = datetime.utcnow() - timedelta(seconds=(INTERVAL * 2))
        double_interval = pytz.timezone('UTC').localize(double_interval).astimezone(pytz.timezone(DEFAULT_TIMEZONE))
        online = last_moisture > double_interval if last_moisture else False
        watering = get_watering_for_pot(watering_, p['id'])
        frequency = get_frequency(watering)
        last_water = human_date(watering[0]['created'] if len(watering) else None)
        result.append({'id': p['id'],
                       'name': p['name'],
                       'description': p['description'],
                       'created': p['created'],
                       'water_value': p['water_value'],
                       'moisture_value': p['moisture_value'],
                       'online': online,
                       'moisture': '{0:.2f}'.format(moisture),
                       'last_water': last_water,
                       'moistures': moistures,
                       'graph': [m['value'] for m in moistures],
                       'graph_labels': ['{} @ {}H'.format(round(m['value'], 2), m['created_real'].strftime('%H')) for m in moistures],
                       'watering': watering,
                       'frequency': frequency
                       })
    dt = pytz.timezone('UTC').localize(datetime.utcnow())
    return {'data': result, 'server_time': dt.astimezone(pytz.timezone(DEFAULT_TIMEZONE)).strftime('%Y-%m-%d %H:%M:%S')}


def get_moisture_for_pot(many, id):
    result = []
    for m in many:
        if m['pot_id'] != id:
            continue
        dt = pytz.timezone('UTC').localize(m['created'])
        result.append({'value': m['value'],
                       'created': human_date(dt.astimezone(pytz.timezone(DEFAULT_TIMEZONE))),
                       'created_real': dt.astimezone(pytz.timezone(DEFAULT_TIMEZONE))
                       })
    return result


def get_watering_for_pot(many, id):
    result = []
    for m in many:
        if m['pot_id'] != id:
            continue
        dt = pytz.timezone('UTC').localize(m['created'])
        result.append({'id': m['id'],
                       'value': m['value'],
                       'description': m['description'],
                       'created': human_date(dt.astimezone(pytz.timezone(DEFAULT_TIMEZONE))),
                       'created_real': dt.astimezone(pytz.timezone(DEFAULT_TIMEZONE))
                       })
    return result


def human_date(date):
    if not date:
        return None
    if isinstance(date, str):
        return date
    now = pytz.timezone('UTC').localize(datetime.utcnow())
    now = now.astimezone(pytz.timezone(DEFAULT_TIMEZONE))
    if date.strftime('%Y-%m-%d') == now.strftime('%Y-%m-%d'):
        return 'today at {}'.format(date.strftime("%H:%M:%S"))
    elif date.strftime('%Y-%m-%d') == (now - timedelta(days=1)).strftime('%Y-%m-%d'):
        return 'yesterday at {}'.format(date.strftime("%H:%M:%S"))
    return date.strftime("%Y-%m-%d at %H:%M:%S")


def get_frequency(watering):
    sum = timedelta()
    count = 0
    last = None
    for w in watering:
        if last:
            sum += w['created_real'] - last
            count += 1
        last = w['created_real']
    if count > 0:
        avg = sum / count
        if avg.seconds < 60:
            return '{} seconds'.format(avg.seconds)
        if avg.seconds / 60 < 60:
            return '{} minutes'.format(avg.seconds)
        hours = round(avg.seconds / 3600)
        return '{} hours'.format(hours)

    return None


@bp.route('/eject/<int:pot_id>', methods=('POST',))
@login_required
def eject(pot_id):
    message = Message({'pot_id': pot_id,
                       'control_message': True,
                       'command': 'force_stop'})
    producer = DMSProducer()
    producer.submit(MOISTURE_TOPIC, message)
    return {'pot_id': pot_id,
            'command': 'eject'}


@bp.route('/force/<int:pot_id>', methods=('POST',))
def force(pot_id):
    token_string = request.headers.get('authorization', False)
    if not is_valid_authorization_string(token_string):
        return jsonify(error=403, text='Unauthorized'), 403
    db = get_db()
    pot = db.execute(
        'SELECT water_value FROM pot p WHERE id = ?',
        (pot_id,)
    ).fetchone()

    if not pot:
        return {'pot_id': pot_id,
                'error': 'Pot not found',
                'command': 'force'}
    value = pot['water_value']

    message = WaterMessage({'pot_id': pot_id,
                            'value': value,
                            'created': str(datetime.now()),
                            'description': 'Watering by request, moisture value {}'.format(value)})
    producer = DMSProducer()
    producer.submit(WATER_TOPIC, message)
    return {'pot_id': pot_id,
            'value': value,
            'command': 'force'}
