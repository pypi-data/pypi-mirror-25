""" SunriseCloud Python API """
""" Version 1.0 """
""" Author: Integra """
""" Licence: None """
""" Dev: Partha """

import requests
from django.conf import settings

CLOUD_ORIGIN = settings.CLOUD_ORIGIN
CLOUD_ACCESS_KEY_ID = settings.CLIENT_ID
CLOUD_SECRET_KEY = settings.CLIENT_SECRET

class SunriseCloud(object):

    http_origin = ''
    client_id = ''
    client_secret = ''
    access_token = ''
    is_authorized = False

    def __init__(self, *args, **kwargs):
        """ Initiate parameters "access_key, secret_key, http_origin """

        self.http_origin = CLOUD_ORIGIN
        self.client_id = CLOUD_ACCESS_KEY_ID
        self.client_secret = CLOUD_SECRET_KEY
        self.is_authorized, self.access_token = self._getAccessToken()

    def _getAccessToken(self, *args, **kwargs):
        """ This is an internal method to get the access token """
        
        self.url = self.http_origin + 'cloud/o/token/'
        data = {
            'grant_type' : 'client_credentials',
            'scope':'write'
        }
        # import pdb;pdb.set_trace()

        resp = requests.post(self.url, data = data, verify=False, auth = (self.client_id, self.client_secret))
        if resp.status_code == 200:
            return (True, resp.json()['access_token'])
        else:
            return (False, "Problem in authenticating your request")


    def _get(self, params = None):
        """ Internal method to get the URL """

        headers = {
            'Authorization' : 'Bearer ' + self.access_token
        }
        resp = requests.get(self.http_origin + self.url, verify=False, headers = headers, params = params)
        
        if resp.status_code == 200:
            return (True, resp.json())
        else:
            return (False, 'Resource not found')


    def _post(self, data = None):
        """ Internal method to post the URL """

        headers = {
            'Authorization' : 'Bearer ' + self.access_token
        }
        resp = requests.post(self.http_origin + self.url, verify=False, headers = headers, data = data)
        
        if resp.status_code == 200:
            return (True, resp)
        else:
            return (False, 'Resource not found')


    def read(self, item_path = None):
        """ Read the specified path """

        glue = {'q':''}
        if item_path is not None and item_path.startswith("/"):
            item_path = item_path[1:]
        
        self.url = "cloud/oauth/read/"
        
        if item_path != None:
            glue = {'q': item_path}
        
        return self._get(params = glue)


    def write(self, source, item_name, item_type, size="", origin = "RECON", fileObj=None):
        """ Write file/folder into sunrise cloud """
        # if fileObj is not None:
        if source == None or item_name == None or item_type == None:
            return "Please specify source, item_name, item_type"
        if source == "" or item_name == "" or item_type == "":
            return "Please specify source, item_name, item_type"
        if item_type != "File" and item_type != "Directory":
            return "Invalid item type"
        if source.startswith("/"):
            source = source[1:]

        data = {
            'source': source,
            'item_name' : item_name, 
            'item_type' : item_type,
            'size':size,
            'origin':origin
        }

        self.url = "cloud/oauth/write/"
        return self._post(data = data)
        

    def build(self, item_path):
        """ Build the the if doesn't exists """

        if item_path == None or item_path == "":
            return "Please specify item path"

        data = {
            'item_path': item_path
        }

        self.url = "cloud/oauth/build/"
        return self._post(data = data)

    def rename(self, item_path, new_name, item_type):
        """ Rename the specified item """
        if item_path == None or item_path == "":
            return "Please specify item path"

        data = {
            'item_path': item_path,
            'new_name': new_name,
            'item_type':item_type
        }

        self.url = "cloud/oauth/rename/"
        return self._post(data = data)

        

    def delete(self, item_path):
        """ Delete the specified item """
        
        if item_path == None or item_path == "":
            return "Please specify item path"

        data = {
            'item_path': item_path
        }

        self.url = "cloud/oauth/delete/"
        return self._post(data = data)
        
    def copy(self, source, destination):
        """ Delete the specified item """
        
        if source == None or source == "":
            return "Please specify source path"

        if destination == None or destination == "":
            return "Please specify destination path"

        if source.startswith("/"):
            source = source[1:]

        if destination.startswith("/"):
            destination = destination[1:]
        

        data = {
            'source': source, 
            'destination': destination
        }

        self.url = "cloud/oauth/copy/"
        return self._post(data = data)

    def cut(self, source, destination):
        """ Delete the specified item """
        
        if source == None or source == "":
            return "Please specify source path"

        if destination == None or destination == "":
            return "Please specify destination path"

        if source.startswith("/"):
            source = source[1:]

        if destination.startswith("/"):
            destination = destination[1:]
        

        data = {
            'source': source, 
            'destination': destination
        }

        self.url = "cloud/oauth/cut/"
        return self._post(data = data)
        



