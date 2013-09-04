try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import json
import requests
import urllib


class AzureRequest(object) :
    TOKEN_ENDPOINT = "https://datamarket.accesscontrol.windows.net/v2/OAuth2-13"

    def __init__(self, client_id=None, client_secret=None, scope=None) :
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
    def get_token(self) :
        params = {'grant_type' : 'client_credentials',
                  'client_id' : self.client_id,
                  'client_secret' : self.client_secret,
                  'scope' : self.scope}
        data = urllib.urlencode(params)
        response = requests.post(self.TOKEN_ENDPOINT, data=data)
        jsonresp = json.loads(response.text)
        return "Bearer " + jsonresp['access_token']

class Translator(object) :
    SERVICE_URL = "http://api.microsofttranslator.com/v2/Http.svc/Translate"
    SERVICE_SCOPE = "http://api.microsofttranslator.com"

    def __init__(self, client_id=None, client_secret=None) :
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_requester = AzureRequest(client_id=self.client_id,
                                            client_secret = self.client_secret,
                                            scope=self.SERVICE_SCOPE)
    def translate(self, lang_from=None, lang_to="en", query=None) :
        token = self.token_requester.get_token()
        headers = {'Authorization' : token}
        params = {'text' : query,
                  'to' : lang_to,
                  'from' : lang_from}
        url = self.SERVICE_URL + '?' + urllib.urlencode(params)
        response = requests.get(url, headers=headers)
        response_xml = ET.fromstring(response.text)
        return response_xml.text
        

        
    
