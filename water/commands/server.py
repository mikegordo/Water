import click
from flask.cli import with_appcontext

from water.core.server_consumer import ServerConsumer
from water.db import get_db, close_db
from water.logger import app


@click.command('start_server_consumer')
@with_appcontext
def start_server_consumer():
    app.logger.info('=' * 37)
    app.logger.info('Command start_server_consumer started')
    db = get_db()
    consumer = ServerConsumer(db, broker=None, group='server-group')
    consumer.start()
    app.logger.info('Command start_server_consumer finished')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(start_server_consumer)
