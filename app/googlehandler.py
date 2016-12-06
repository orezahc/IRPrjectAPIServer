# Imports

import aiohttp
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
import pprint


# Constants

API_KEY = 'AIzaSyDCxN6faBfPjZFMJumlb-93DMYVQo3wC3Q'
BASE_URI = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={placeid}&key={key}'
_logger = logging.getLogger(__name__)


# Handlers

class GoogleHandler(tornado.web.RequestHandler):

    def initialize(self, key):
        self._api_key = key
        _logger.info('Google API secret key {}.'.format(self._api_key))

    async def _getPlace(self, google_places, raw_response, i):
        output = {}
        result = raw_response['results'][i]
        uri = BASE_URI.format(key=self._api_key, placeid=result['place_id'])

        response = await aiohttp.get(uri)
        data = await response.text()
        data = json.loads(data)
        output['name'] = data['result']['name']
        output['contact'] = {
            'url': data['result']['website'], 
            'address': data['result']['formatted_address'],
            'phone': data['result']['formatted_phone_number']
        }
        output['open'] = data['result']['opening_hours']['open_now']
        output['geometry'] = {
            'lat': float(data['result']['geometry']['location']['lat']),
            'lng': float(data['result']['geometry']['location']['lng'])
        }

        try:
            output['rating'] = float(data['result']['rating'])
        except:
            output['rating'] = ''

        try:
            output['price'] = float(result['price_level'])
        except:
            output['price'] = ''
            
        return output


    async def _googlePlaceGet(self, key_str = None, location='Seattle'):
        google_places = GooglePlaces(self._api_key)

        if key_str != '':
            query_result = google_places.nearby_search(
                keyword=key_str,
                location=location,
                radius=20000,
                types=[types.TYPE_RESTAURANT])
        else:
            query_result = google_places.nearby_search(
                location=location,
                radius=20000,
                types=[types.TYPE_RESTAURANT])

        datadict = []
        n_queries = len(query_result.raw_response['results'])
        if n_queries > 3:
            n_queries = 3

        tasks = [self._getPlace(google_places, query_result.raw_response, i)
                    for i in range(n_queries)]

        for data in asyncio.as_completed(tasks):
            datadict.append(await data)

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

        data = await self._googlePlaceGet(key_str=restaurantName)
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
