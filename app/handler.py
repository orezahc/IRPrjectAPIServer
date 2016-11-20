# Imports

import asyncio
import json
import logging
import time
import tornado
import tornado.ioloop
import tornado.web
import bunyan
import os
import sys

_logger = logging.getLogger(__name__)

# Handlers

class Handler(tornado.web.RequestHandler):

    async def get(self, restaurantName):
        '''
        Receives ACK of scores from phillips to ensures the scores sent from us
        are received.

        Parameters
        ----------
        correlationId : str
            The correlation id associated to the ACK of scores.
        '''
        self.set_status(200)
        self.finish('Received request : {}'.format(restaurantName))

