# Imports

import asyncio
import tornado
import tornado.web
import tornado.platform.asyncio
import googlehandler
import yelphandler
import bunyan
import logging
import os
import sys

import argparse
import googlehandler
import yelphandler

_PRETTY_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s'
_logger = logging.getLogger(__name__)

# Setup

def _setup(key):
    '''
    Sets up web routes handler.
    '''
    # Set up logger
    logHandler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(_PRETTY_FORMAT)
    logHandler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(logHandler)
    logger.setLevel(10)

    # Set up tornado to use the asyncio event loop.
    mainLoop = tornado.platform.asyncio.AsyncIOMainLoop().install()
    ioloop = asyncio.get_event_loop()

    print(key)
    app = tornado.web.Application([
        (r"/api/google/(?P<restaurantName>.*)", googlehandler.GoogleHandler, dict(key=key)),
        (r"/api/yelp/(?P<restaurantName>.*)", yelphandler.YelpHandler)
    ])

    app.listen(80)

    # Go!
    logging.getLogger(__name__).info('Entering IO loop.')
    ioloop.run_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Search API'
    )

    parser.add_argument(
        '-log-level',
        type=int,
        default=logging.INFO,
        choices=[
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL
        ],
        help='The logging message threshold.'
    )

    parser.add_argument(
        '-secret-key',
        type=str,
        help='Api key.'
    )

    args = parser.parse_args()
    _setup(args.secret_key)
