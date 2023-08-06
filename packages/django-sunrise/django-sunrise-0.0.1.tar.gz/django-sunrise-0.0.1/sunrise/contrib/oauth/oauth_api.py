""" RESTAPI Python API """
""" Version 1.0 """
""" Author: Integra """
""" Licence: None """
""" Dev: Partha """

import requests

class RESTApi(object):
    """ This is the genric RESTApi python API, using this you can connect with any REST API Endpoint using creds """
    
    access_token = None
    is_authorized = False

    def __init__(self, *args, **kwargs):
        """ Initiate parameters "access_key, secret_key, http_origin """
        if 'access_token' in kwargs.keys():
            self.access_token = kwargs['access_token']
            self.ORIGIN = kwargs['ORIGIN']        
            if self.ORIGIN.endswith("/"):
                self.ORIGIN = self.ORIGIN[:-1]
        else:
            assert('ORIGIN' in kwargs.keys()), "Prvide ORIGIN in kwargs"
            assert('CLIENT_ID' in kwargs.keys()), "Prvide CLIENT_ID in kwargs"
            assert('CLIENT_SECRET' in kwargs.keys()), "Prvide CLIENT_SECRET in kwargs"
            
            self.ORIGIN = kwargs['ORIGIN']                
            self.CLIENT_ID = kwargs['CLIENT_ID']
            self.CLIENT_SECRET = kwargs['CLIENT_SECRET']
            self.is_authorized, self.access_token = self._getAccessToken()

    def _getAccessToken(self, *args, **kwargs):
        """ This is an internal method to get the access token """
        if self.ORIGIN.endswith("/"):
            self.ORIGIN = self.ORIGIN[:-1]
        self.url = self.ORIGIN + '/o/token/'
        data = {
            'grant_type' : 'client_credentials',
            'scope':'write'
        }
        resp = requests.post(self.url, data = data, verify=False, auth = (self.CLIENT_ID, self.CLIENT_SECRET))
        if resp.status_code == 200:
            # self.request.session['portal_access_token'] = resp.json()['access_token']
            return (True, resp.json()['access_token'])
        else:
            return (False, "Problem in authenticating your request")

    def _response_handler(self, response):
        """ This is used to handle the response """
        if response.status_code == 200:
            return (True, response.json())
        if response.status_code == 201:
            return (True, response.json())
        if response.status_code == 403:
            return (False, "Restricted Access, please contact Administrator")
        if response.status_code == 404:
            return (False, "Resource not found")
        if response.status_code == 500:
            return (False, "Something went wrong, please report to Administrator")
        if response.status_code == 401:
            return (False, "Token Expired")            
        return (False, 'Resource not found')

    def _get(self, url, params = None, prefix="RemoteAPI"):
        """ Internal method to get the URL """
        headers = {
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer ' + self.access_token,
            'X-GridKey':prefix
        }
        response = requests.get(self.ORIGIN + url, verify=False, headers = headers, params = params)
        return self._response_handler(response)

    def _post(self, url, data = None):
        """ Internal method to post the URL """
        headers = {
            'Content-Type': 'application/json',            
            'Authorization' : 'Bearer ' + self.access_token,
        }
        response = requests.post(self.ORIGIN + url, verify=False, headers = headers, json = data)
        return self._response_handler(response)        
    
    def _put(self, url, data = None):
        """ Internal method to post the URL """ 
        headers = {
            'Content-Type': 'application/json',           
            'Authorization' : 'Bearer ' + self.access_token,
        }
        response = requests.put(self.ORIGIN + url, verify=False, headers = headers, json = data)
        return self._response_handler(response)
        

    def _delete(self, url, data = None):
        """ Internal method to post the URL """
        headers = {
            'Content-Type': 'application/json',            
            'Authorization' : 'Bearer ' + self.access_token,
        }
        response = requests.delete(self.ORIGIN + url, verify=False, headers = headers, json = data)
        return self._response_handler(response)    

    def list(self, resource = None, params = None, prefix=None):
        """ REST based LIST 
            @param: resource (required)
            @param: params (optional) """
        assert(resource is not None), "Please provide resource name, parameter 'resource' is missing. Ex: resource='/api/setup/<resource>/'"
        return self._get(resource, params = params, prefix=prefix)

    def retrieve(self, resource = None, ID = None, params = None):
        """ REST based RETRIEVE
            @param: resource (required)
            @param: ID (required)
            @param: params (optional) """
        assert(resource is not None), "Please provide resource name, parameter 'resource' is missing. Ex: resource='/api/setup/<resource>/'"
        assert(ID is not None), "Please provide item lookup parameter, parameter 'ID' is missing. Ex: ID=1"
        resource = resource + ID + "/"
        return self._get(resource, params = params)

    def create(self, resource=None, data=None):
        """ REST based create 
            @param: resource (required)
            @param: data (required) """
        assert(resource is not None), "Please provide resource name, parameter 'resource' is missing. Ex: resource='/api/setup/<resource>/'"        
        assert(data is not None), "Please provide data to insert"
        return self._post(resource, data = data)
        
    def update(self, resource=None, ID=None, data=None):
        """ REST based update 
            @param: resource (required)
            @param: data (required) """
        assert(resource is not None), "Please provide resource name, parameter 'resource' is missing. Ex: resource='/api/setup/<resource>/'"        
        assert(ID is not None), "Please provide resource name, parameter 'resource' is missing. Ex: resource='/api/setup/<resource>/'"                
        assert(data is not None), "Please provide data to insert"
        resource = resource + ID + "/"
        return self._put(resource, data = data)

    def delete(self, resource=None, ID=None):
        """ REST based create 
            @param: resource (required)
            @param: data (optional) """
        assert(resource is not None), "Please provide resource name, parameter 'resource' is missing. Ex: resource='/api/setup/<resource>/'"        
        assert(ID is not None), "Please provide resource name, parameter 'resource' is missing. Ex: resource='/api/setup/<resource>/'"                
        resource = resource + "/" + ID
        return self._delete(resource, data = data)



class SunriseBillingAPI(RESTApi):
    """ You can have your own presets here """
    pass
    
