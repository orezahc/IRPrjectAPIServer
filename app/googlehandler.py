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
import pprint


# Constants

API_KEY = 'AIzaSyDCxN6faBfPjZFMJumlb-93DMYVQo3wC3Q'
_logger = logging.getLogger(__name__)


# Handlers

class GoogleHandler(tornado.web.RequestHandler):

    def _googlePlaceGet(self, keyStr = None, location='Seattle'):
        google_places = GooglePlaces(API_KEY)

        if keyStr == '':
            query_result = google_places.nearby_search(
                keyword=keyStr,
                location=location,
                radius=20000,
                types=[types.TYPE_RESTAURANT])
        else:
            query_result = google_places.nearby_search(
                location=location,
                radius=20000,
                types=[types.TYPE_RESTAURANT])

        pp = pprint.PrettyPrinter(indent=4)

        datadict = []
        for result in query_result.raw_response['results']:
            data = {}
            place = google_places.get_place(place_id=result['place_id']).details
            data['name'] = place['name']
            try:
                data['rating'] = float(place['rating'])
            except:
                data['rating'] = ''

            data['contact'] = {
                'url': place['url'], 
                'address': place['formatted_address'],
                'phone': place['formatted_phone_number']
            }
            data['open'] = place['opening_hours']['open_now']
            try:
                data['price'] = float(result['price_level'])
            except:
                data['price'] = ''
                
            data['geometry'] = {
                'lat': float(place['geometry']['location']['lat']),
                'lng': float(place['geometry']['location']['lng'])
            }
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

        data = self._googlePlaceGet(keyStr=restaurantName)
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
