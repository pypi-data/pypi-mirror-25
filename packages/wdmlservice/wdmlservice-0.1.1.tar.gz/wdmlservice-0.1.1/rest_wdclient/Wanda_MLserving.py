import requests
from requests import ConnectionError
from base64 import b64encode


WD_MLserving_TIMEOUT = 2000  # seconds, for long blocking training calls, as needed

API_METHODS_URL = {
    "0.1": {
        "info": "/info",
        "services": "/services",
        "train": "/train",
        "predict": "/predict"
    }
}

class Wanda_MLserving(object):
    """HTTP requests to the Wanda_ML server
    """
    # return types
    RETURN_PYTHON = 0
    RETURN_JSON = 1
    RETURN_NONE = 2
    
    __HTTP = 0
    __HTTPS = 1
    def __init__(self, host="127.0.0.1", port=5412,model_pool_path='predict', proto=0, apiversion="0.1",auth_token=None):
        """ DD class constructor
        Parameters:
        host -- the Wanda_ML server host
        port -- the Wanda_ML server port
        proto -- user http (0,default) or https connection
        """
        self.apiversion = apiversion
        self.__urls = API_METHODS_URL[apiversion]
        self.__host = host
        self.__port = port
        self.__proto = proto
        self.__returntype = self.RETURN_PYTHON
        self.auth_token = auth_token
        self.__model_pool_path=model_pool_path
        if proto == self.__HTTP:
            self.__wdurl = 'http://%s:%d' % (host, port)
        else:
            self.__wdurl = 'https://%s:%d' % (host, port)
    def __getattr__(self, func_name):
        print 'func_name',func_name
        return RemoteFunction(self, func_name)

    def call_func(self, func_name, **kwargs):
        path = func_name
        return self.post(path, **kwargs)
    
    def prepare_headers(self):
        """Prepares headers for sending a request to the Wanda_ML server.
        """
        headers = {}
        headers['Content-type']= "application/json"
        headers['Accept'] = 'application/json'
        if self.auth_token:
            headers['Authorization'] = 'Basic ' + b64encode((self.auth_token['username'] + ':' + self.auth_token['password'])
                                                        .encode('utf-8')).decode('utf-8')
        return headers
    def set_return_format(self, f):
        assert f == self.RETURN_PYTHON or f == self.RETURN_JSON or f == self.RETURN_NONE
        self.__returntype = f
    def set_return_format(self, f):
        assert f == self.RETURN_PYTHON or f == self.RETURN_JSON or f == self.RETURN_NONE
        self.__returntype = f

    def __return_data(self, r):
        if self.__returntype == self.RETURN_PYTHON:
            return r.json()
        elif self.__returntype == self.RETURN_JSON:
            return r.text
        else:
            return None
    def get(self, method, json='machine learning serving is running', params=None):
        """GET to DeepDetect server """
        url = self.__wdurl + method
        r = requests.get(url=url, json=json, params=params, timeout=WD_MLserving_TIMEOUT)
        r.raise_for_status()
        return self.__return_data(r)
    def post(self,_path,**kwargs):
        """POST request to Wanda_ML server"""
        try:
            headers = self.prepare_headers()
            url = self.__wdurl +'/'+self.__model_pool_path+'/'+ _path
            print url
            data, files = self.decouple_files(kwargs)
            #if file:data,if json:json
            r = requests.post(url=url, json=data, headers=headers,timeout=WD_MLserving_TIMEOUT)
            r.raise_for_status()
        except ConnectionError:
            MlservingError('Unable to connect to the server, please try again later.')
        return self.__return_data(r)
    def decouple_files(self, kwargs):
        data = {arg: value for arg, value in kwargs.items() if not self.is_file(value)}
        files = {arg: value for arg, value in kwargs.items() if self.is_file(value)}
        return data, files

    def is_file(self, value):
        return hasattr(value, 'read') or hasattr(value, 'readlines')
    # API methods
    def info(self):
        """Info on the DeepDetect server"""
        return self.get(self.__urls["info"])
def RemoteFunction(client, func_name):
    def wrapped(**kwargs):
        return client.call_func(func_name, **kwargs)
    wrapped.__name__ = func_name
    wrapped.__qualname__ = func_name
    return wrapped
class MlservingError(Exception):
    pass