import os
import argparse
from os import path

from vexmessage import decode_vex_message
from vexbot.util.messaging import get_addresses

import zmq

from vexstorage.database import DatabaseManager
from vexstorage.database import create_database as _create_database

try:
    import setproctitle
    setproctitle.setproctitle('vexstorage')
except ImportError:
    pass


def run(database_filepath: str=None, addresses: list=None):
    if database_filepath is None:
        database_filepath = _get_database_filepath()
    if addresses is None:
        addresses = ['tcp://127.0.0.1:4001']

    database = DatabaseManager(database_filepath)
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b'')
    for address in addresses:
        socket.connect(address)
    while True:
        frame = socket.recv_multipart()
        try:
            msg = decode_vex_message(frame)
        except Exception:
            continue

        if msg.type == 'MSG':
            author = msg.contents.get('author', msg.source)
            contents = msg.contents.get('message', None)
            if contents and author:
                database.record_message(msg.source,
                                        author,
                                        contents)


def create_database():
    kwargs = _get_kwargs()
    _create_database(kwargs['database_filepath'])


def _get_kwargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('database_filepath',
                        action='store',
                        default=None)

    parser.add_argument('--addresses', help='zmq addresses to subscribe to',
                        nargs='*',
                        default=None)

    return vars(parser.parse_args())

def main(*args, **kwargs):
    program_kwargs = _get_kwargs()
    kwargs.update(program_kwargs)
    run(**kwargs)

if __name__ == '__main__':
    main()
