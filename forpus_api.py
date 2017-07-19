# coding: utf-8

import requests, json, string, random
from datetime import datetime
from functools import wraps

def ensure_auth(f):
    """ makes sure the client has a valid token
    when a function is called
    """
    def wrapper(*args):
        result = f(*args)
        if type(result) is dict and 'error' in result and \
		result['error'] == 'Not Authorized':
            args[0].authenticate()
            return f(*args)
        return result
    return wrapper

class Forpus(object):
    """ A client for the Forpus App Rest API
    It provides methods for updating the Web App with fresh market data
    """
    
    def __init__(self, *args):
        """
        There are two possible constructors.
        
        The first one expects user and password strings for the Forpus Rest API
        
        >> from forpus_api import Forpus
        >> feeder = Forpus('user', 'password')
        
        The second one expects to find environment variables:
        
        FORPUSAPI_USER
        FORPUSAPI_PASSWORD
        
        >> import os
        >> from forpus_api import Forpus
        >> feeder = Forpus(os.environ)
        
        """
        if len(args) == 2:
            try:
                self.user = args[0]
                self.password = args[1]
            except:
                raise Exception('Expected user and password')
        else:
            try:
                self.user = args[0]['FORPUSAPI_USER']
                self.password = args[0]['FORPUSAPI_PASSWORD']
            except:
                raise Exception("Make sure you provide os.envon, also " + \
                                "FORPUSAPI_USER and FORPUSAPI_PASSWORD " + \
                                "environment variables are expected to " + \
                                "be defined")
        self.token = ''
        self.session = requests.Session()
    
    def api_url(self, path):
        """ this base url must be set in an environment variable
        depending on target environment (development, test, production)
        """
        base_url = "https://forpus-thiagolcmelo.c9users.io/api/v1"
        return "%s/%s" % (base_url, path)

    def parse_response(self, text):
        """ the response is expected to be a json, but there are some
        cases when trash html is still been received, meanwhile,
        let's keep this
        """
        try:
            return json.loads(text)
        except ValueError:
            raise Exception('Invalid response, shame on me, sorry...')

    def authenticate(self):
        """ authenticates the client against the Forpus API
        it already sets the session authorization header with
        the valid token received if successful
        """
        payload = {
            "email": self.user,
            "password": self.password
        }
        r = self.session.post(self.api_url("authenticate"), data=payload)
        response = self.parse_response(r.text)
        if (type(response) is dict and 'error' in response) or \
		not 'auth_token' in response:
            raise Exception(response['error'])
        self.token = json.loads(r.text)["auth_token"]
        self.session.headers = {"Authorization": self.token }

    @ensure_auth
    def get(self, path, params={}):
        r = self.session.get(self.api_url(path), params=params)
        return self.parse_response(r.text)

    @ensure_auth
    def post(self, path, payload={}):
        r = self.session.post(self.api_url(path), json=payload)
        return self.parse_response(r.text)

    @ensure_auth
    def patch(self, path, obj_id, payload):
        patch_url = self.api_url("%s/%d" % (path, int(obj_id)))
        r = self.session.patch(patch_url, json=payload)
        return self.parse_response(r.text)
    
    @ensure_auth
    def delete(self, path, obj_id):
        delete_url = self.api_url("%s/%d" % (path, int(obj_id)))
        r = self.session.delete(delete_url)
        return self.parse_response(r.text)

    # METHODS FOR DEALING WITH SECURITIES
    def list_securities(self):
        return self.get('securities')

    def create_security(self, security):
        return self.post('securities', security)

    def update_security(self, security):
        return self.patch('securities', security['security']['id'], security)

    def delete_security(self, security_id):
        return self.delete('securities', security_id)

    # METHODS FOR DEALING WITH SECURITY TYPES
    def list_security_types(self):
        return self.get('security_types')

    def create_security_type(self, security_type):
        return self.post('security_types', security_type)

    def update_security_type(self, security_type):
        return self.patch('security_types', \
		security_type['security_type']['id'], security_type)

    def delete_security_type(self, security_type_id):
        return self.delete('security_types', security_type_id)

    # METHODS FOR DEALING WITH FREQUENCIES
    def list_frequencies(self):
        return self.get('frequencies')

    def create_frequency(self, frequency):
        return self.post('frequencies', frequency)

    def update_frequency(self, frequency):
        return self.patch('frequencies', frequency['frequency']['id'], frequency)

    def delete_frequency(self, frequency_id):
        return self.delete('frequencies', frequency_id)

    # METHODS FOR DEALING WITH PRICE TYPES
    def list_price_types(self):
        return self.get('price_types')

    def create_price_type(self, price_type):
        return self.post('price_types', price_type)

    def update_price_type(self, price_type):
        return self.patch('price_types', price_type['price_type']['id'], price_type)

    def delete_price_type(self, price_type_id):
        return self.delete('price_types', price_type_id)

    # METHODS FOR DEALING WITH PRICES
    def list_prices(self):
        return self.get('prices')

    def create_price(self, price):
        return self.post('prices', price)

    def update_price(self, price_type):
        return self.patch('prices', price['price']['id'], price)

    def delete_price(self, price_id):
        return self.delete('prices', price_id)

    def filter_prices(self, **kwargs):
        """ the filter allowed params are:
        - security_id: (int), required
        - price_type_id: (int), required
        - start_date: 'yyyy-mm-dd', optional
        - end_date: 'yyyy-mm-dd', optional
        - limit: (int), optional, (max = defaulf = 1000)
        - order: ['asc', 'desc'], optional, (default = 'desc')
        """
        return self.get('filter_price', kwargs) 

    # METHODS FOR DEALING WITH TIME WEIGHTS
    def list_time_weights(self):
        return self.get('time_weights')

    def create_time_weight(self, time_weight):
        return self.post('time_weights', time_weight)

    def update_time_weight(self, time_weight):
        return self.patch('time_weights', time_weight['time_weight']['id'], time_weight)

    def delete_time_weight(self, time_weight_id):
        return self.delete('time_weights', time_weight_id)

    # METHODS FOR DEALING WITH TIME VOLUMES
    def list_time_volumes(self):
        return self.get('time_volumes')

    def create_time_volume(self, time_volume):
        return self.post('time_volumes', time_volume)

    def update_time_volume(self, time_volume):
        return self.patch('time_volumes', time_volume['time_volume']['id'], time_volume)

    def delete_time_volume(self, time_volume_id):
        return self.delete('time_volumes', time_volume_id)
