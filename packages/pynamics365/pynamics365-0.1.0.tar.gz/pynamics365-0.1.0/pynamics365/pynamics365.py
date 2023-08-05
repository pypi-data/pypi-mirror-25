# -*- coding: utf-8 -*-
"""Main module."""
import os
import sys
import logging
from getpass import getpass
from configparser import ConfigParser
import requests

from pynamics365 import auth
logging.basicConfig(level=logging.DEBUG)

class Pynamics365():
    """Class to handle authentication and requests on the Dynamics 365 Web API."""
    def __init__(self, crmorg="", clientid="", username="", password="", tokenendpoint="", crmwebapi=""):
        self.config_file = "settings.ini"
        self.crmorg = crmorg
        self.clientid = clientid
        self.username = username
        self.password = password
        self.tokenendpoint = tokenendpoint
        self.crmwebapi = crmwebapi
        if self.crmorg == "":  # Assume no settings passed
            self.load_config()
        self.access_token = auth.get_access_token(self.crmorg, self.clientid, self.username, self.password, self.tokenendpoint)
        self.crmrequestheaders =  {
            'Authorization': 'Bearer ' + self.access_token,
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
            'Prefer': 'odata.maxpagesize=500',
            'Prefer': 'odata.include-annotations=OData.Community.Display.V1.FormattedValue'
        }


    def load_config(self):
        """Loads configuration from a file."""
        logging.debug("load_config")
        if not os.path.isfile(self.config_file):
            self.create_config()
            logging.info(f"Settingsfile created. Please fill details in {settingsfile}")
            sys.exit()
        config = ConfigParser()
        config.read(self.config_file)
        config_dict = dict(config.items('AUTHENTICATION'))
        self.crmorg = config_dict['crmorg']
        self.clientid = config_dict['clientid']
        self.username = config_dict['username']
        if "password" not in config_dict or config_dict['password'] == '':
            self.password = getpass()
        else:
            self.password = config_dict['password']
        self.tokenendpoint = config_dict['tokenendpoint']
        self.crmwebapi = config_dict['crmwebapi']


    def create_config(self):
        """Creates a configuration file."""
        logging.debug("create_config")
        config = ConfigParser()
        config['AUTHENTICATION'] = {
            'crmorg' : '',
            'clientid' : '',
            'username' : '',
            'password' : '',
            'tokenendpoint' : '',
            'crmwebapi' : ''
        }
        with open(self.config_file, "w") as configfile:
            config.write(configfile)


    def retrieve_record(self, record_id, entity_type, select=None, expand=None):
        """
        Retrieves a single records.

        Keyword arguments:
        record_id -- the id of the record.
        entity_type -- the record's entity type.
        select -- not tested yet.
        expand -- not tested yet.
        """
        logging.debug("retrieve_record")
        options = { "$select": select, "$expand": expand }
        query = "/{0}({1}){2}".format(entity_type, record_id, self.get_options_string(options))
        response = requests.get(self.crmwebapi+query, headers=self.crmrequestheaders)
        try:
            result = response.json()
            return result["value"]
        except KeyError as err:
            logging.error(err)


    def retrieve_multiple_records(self, entity_type, select=None, expand=None, where=None):
        """
        Retrieves multiple records.

        Keyword arguments:
        entity_type -- entitity to retrieve.
        select -- attributes to retrieve from entitiy.
        expand -- not tested yet.
        where -- not tested yet.
        """
        options = { "$select": select, "$expand": expand, "$filter": where }
        query = "/{0}{1}".format(entity_type, self.get_options_string(options))
        response = requests.get(self.crmwebapi+query, headers=self.crmrequestheaders)
        try:
            result = response.json()
            return result["value"]
        except KeyError as err:
            logging.error(err)
    
    def get_options_string(self, options):
        """Builds an option string from key value pairs."""
        query = "&".join("{0}={1}".format(key, val) for key, val in options.items() if val)
        return "?{0}".format(query) if query else ""

if __name__ == "__main__":
    p365 = Pynamics365()
    print(p365.retrieve_multiple_records('contacts', select='fullname'))
