# -*- coding: utf-8 -*-
import logging
import requests

LOGGER = logging.getLogger(__name__)

def get_access_token(crmorg, clientid, username, password, tokenendpoint):
    """
    Logs in and extracts the access token.

    Keyword arguments:
    crmorg -- the base url for the crm organization.
    clientid -- the application client id.
    username -- the username.
    password -- the password.
    tokenendpoint -- the oauth token endpoint.
    """
    LOGGER.debug("get_access_token")
    tokenpost = {
        'client_id':clientid,
        'resource':crmorg,
        'username':username,
        'password':password,
        'grant_type':'password'
    }
    tokenres = requests.post(tokenendpoint, data=tokenpost)
    access_token = ''
    try:
        print(tokenres.json())
        access_token = tokenres.json()['access_token']
    except KeyError as err:
        LOGGER.exception("Key not found in response", err)
    return access_token