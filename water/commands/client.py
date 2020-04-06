import os
from multiprocessing import Process

import click
from flask.cli import with_appcontext

from water.core.client import Client
from water.core.client_configuration import ClientConfiguration
from water.core.client_consumer import ClientConsumer
from water.logger import app


@click.command('start_client')
@click.argument("filename")
@with_appcontext
def start_client(filename):
    app.logger.info('=' * 28)
    app.logger.info('Command start_client started')
    configuration = _get_pi_configuration(filename)
    p = Process(target=client_thread, args=(configuration,))
    p.start()
    consumer = ClientConsumer(configuration)
    consumer.start()
    p.kill()
    app.logger.info('Command start_client finished')


def client_thread(configuration):
    worker = Client(configuration)
    worker.start()


def _get_pi_configuration(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    full_name = '{}/../../configuration/{}'.format(dir_path, filename)
    if not os.path.exists(full_name) or not os.path.isfile(full_name):
        raise Exception('Unable to locate {}'.format(full_name))
    return ClientConfiguration(full_name)


def init_app(app):
    app.cli.add_command(start_client)
    # app.cli.add_command(start_client_consumer)
