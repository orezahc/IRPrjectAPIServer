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
from googleplaces import GooglePlaces, types, lang
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import pprint


# Constants

API_KEY = 'AIzaSyDCxN6faBfPjZFMJumlb-93DMYVQo3wC3Q'
_logger = logging.getLogger(__name__)

YOUR_CONSUMER_KEY='KlDUFYwisNqBpymidMf3RA'
YOUR_CONSUMER_SECRET='7_PkdA-TptR0sm6vplmo2RMl650'
YOUR_TOKEN='IWBrJcXRmEs9t_YUiV182jpNusLTS_c6'
YOUR_TOKEN_SECRET='x8_mBE63WQabSQhBnx2h-GX9SsQ'
    
auth = Oauth1Authenticator(
    consumer_key=YOUR_CONSUMER_KEY,
    consumer_secret=YOUR_CONSUMER_SECRET,
    token=YOUR_TOKEN,
    token_secret=YOUR_TOKEN_SECRET
)

params = {
    'term': 'food',
}


# Handlers

class YelpHandler(tornado.web.RequestHandler):

    def _yelpPlaceGet(self, keyStr = None):
        yelp_places = Client(auth)
        response=client.search(keyStr, **params)

                
        pp = pprint.PrettyPrinter(indent=4)

        datadict = []
        for result in response.businesses:
            data = {"name":str(item.name), 
			"phone":str(item.phone), 
			"url":str(item.url)}
		datadict.append(data)

        pp.pprint(datadict)
        return datadict


    async def get(self, restaurantName):
        '''
        Receives ACK of scores from phillips to ensures the scores sent from us
        are received.

        Parameters
        ----------
        correlationId : str
            The correlation id associated to the ACK of scores.
        '''

        data = self._yelpPlaceGet(keyStr=restaurantName)
        result = {
            'metadata': {
                'keyword': restaurantName,
                'timestamp' : int(time.time())
            },
            'data': data
        }
        self.set_status(200)
        self.set_header('Content-Type', 'application/json; charset="utf-8"')
        self.finish(json.dumps(result))


