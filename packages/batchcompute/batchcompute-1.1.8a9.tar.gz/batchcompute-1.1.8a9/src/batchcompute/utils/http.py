import sys
import datetime

from batchcompute.utils import constants
from .constants import STRING 
from .functions import partial, url_safe, utf8, import_httplib, get_local_ip
from .log import get_logger 

HAVE_HTTPS_CONNECTION = False
try:
    import ssl
    if hasattr(ssl, 'SSLError'):
        HAVE_HTTPS_CONNECTION = True
except ImportError:
    pass 


httplib = import_httplib()
logger = get_logger('batchcompute.utils.http')

class ResponseWrapper(object):
    def __init__(self, response_body, raw_response):
        self.data_ = response_body
        self.raw_ = raw_response

    def read(self):
        return self.data_ 

    def __getattr__(self, attr):
        return getattr(self.raw_, attr)

class RequestClient(object):
    '''
    A simple http client implement.
    '''
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD']

    def __init__(self, host, port):
        self.h, self.p = (host, port)

    def send_request(self, method, path='', params={}, headers={}, body=''):
        # Start args validate sections.
        assert path and isinstance(path, STRING), 'path must be str and may not be Empty'
        assert not params or isinstance(params, dict) or isinstance(params, STRING), 'params must be dict or None'
        assert not params or isinstance(headers, dict), 'headers must be dict or None'
        assert not body or isinstance(body, STRING), 'body must be str or None'
        # Finish args validate sections.

        conn = self.get_http_connection()
        url = self.get_url(path, params)

        logger.debug("Request method: %s\n"
                     "Request url: %s\n"
                     "Request body: %s\n"
                     "Request headers: %s\n",
                     method, url, body, headers)
        # To fix bugs in some Python version.
        for key, val in headers.items():
            headers[key] = str(val)
        conn.request(method, url, body, headers)
        res = conn.getresponse()
        response_body = res.read()
        conn.close()

        return ResponseWrapper(response_body, res) 

    def __getattr__(self, attr):
        if attr.upper() in self.methods:
           return partial(self.send_request, attr.upper())
        else:
            errs = (self.__class__.__name__, attr)
            raise AttributeError("'%s' object has no attribute '%s'"%errs)

    def get_http_connection(self):
        if self.p == constants.SECURITY_SERVICE_PORT and HAVE_HTTPS_CONNECTION:
            if sys.version_info >= (2,7,9) and sys.version_info[0] < 3:
                # Context prrameter was added.
                from ssl import create_default_context as _create_default_context
                ctx = _create_default_context(cafile=None)
                ctx.check_hostname = False
                conn = httplib.HTTPSConnection(self.h, self.p, context=ctx)
            elif sys.version_info[0] >= (3.2):
                conn = httplib.HTTPSConnection(self.h, self.p, check_hostname=False)
            else:
                conn = httplib.HTTPSConnection(self.h, self.p)
        else:
            self.p = constants.SERVICE_PORT  
            conn = httplib.HTTPConnection(self.h, self.p)
        return conn

    def get_url(self, path, params):
        '''
        Generates request url according to specified params.
        '''
        filter_ = ''
        if isinstance(params, dict):
            p = []
            for (k, v) in sorted(params.items()):
                k, v = (url_safe(k.replace('_', '-')), url_safe(utf8(v)))
                entry = "%s=%s"%(k, v) if v.strip() else "%s"%(k)
                if entry:
                    p.append(entry)
            connector = '&'
            filter_ = connector.join(p)
        elif isinstance(params, STRING):
            filter_ = params
        else:
            raise TypeError("params must be string or dict type")

        seperator = '?' if filter_ else ''
        return '%s%s%s'%(path, seperator, filter_)


def mock_pop_headers(raw_header_func):
    '''
    Wrapper function for the interface of get_headers of `Api` object.
    '''
    def mock_pop(raw):
        pop_headers = {}
        pop_headers['HTTP_ACCEPT'] = raw['Accept']
        pop_headers['HTTP_ACCEPT_ENCODING'] = 'identity'
        pop_headers['HTTP_AUTHORIZATION'] = raw['Authorization']
        pop_headers['HTTP_CONTENT_LENGTH'] = str(raw['Content-Length'])
        pop_headers['HTTP_CONTENT_TYPE'] = raw['Content-Type']
        pop_headers['HTTP_DATE'] = raw['Date']
        pop_headers['HTTP_USER_AGENT'] = 'Mozilla/5.0 (Windows NT 6.1)'
        pop_headers['HTTP_WEB_SERVER_TYPE'] = 'nginx'
        pop_headers['HTTP_WL_PROXY_CLIENT_IP'] = pop_headers['HTTP_HOST']
        pop_headers['HTTP_X_ACS_ACCESS_KEY_ID'] = raw['x-acs-access-key-id']
        pop_headers['HTTP_X_ACS_AK_MFA_PRESENT'] = 'false'
        pop_headers['HTTP_X_ACS_API_NAME'] = 'no use'
        pop_headers['HTTP_X_ACS_CALLER_BID'] = '26842'
        pop_headers['HTTP_X_ACS_CALLER_UID'] = '48351'
        #pop_headers['HTTP_X_ACS_CALLER_UID'] = pop_headers['HTTP_HOST']
        pop_headers['HTTP_X_ACS_PROXY_TRUST_TRANSPORT_INFO'] = 'false'
        pop_headers['HTTP_X_ACS_REGION_ID'] = raw['x-acs-region-id']
        # XXX
        pop_headers['HTTP_X_ACS_REQUEST_ID'] = raw['x-acs-signature-nonce']
        pop_headers['HTTP_X_ACS_SECURITY_TRANSPORT'] = 'false'
        pop_headers['HTTP_X_ACS_SIGNATURE_METHOD'] = raw['x-acs-signature-method']
        pop_headers['HTTP_X_ACS_SIGNATURE_NONCE'] = raw['x-acs-signature-nonce']
        pop_headers['HTTP_X_ACS_SIGNATURE_VERSION'] = raw['x-acs-signature-version']
        pop_headers['HTTP_X_ACS_VERSION'] = raw['x-acs-version']
        pop_headers['HTTP_X_FORWARDED_FOR'] = '127.0.0.1'
        pop_headers['HTTP_X_ACS_CALLER_TYPE'] = 'customer'

        pop_headers['x-acs-request-id'] = raw['x-acs-signature-nonce']
        pop_headers['x-acs-version'] = raw['x-acs-version']
        pop_headers['x-acs-caller-uid'] = '48351'
        pop_headers['x-acs-caller-type'] = 'customer'
        pop_headers['x-acs-signature-version'] = raw['x-acs-signature-version']
        pop_headers['x-acs-region-id'] = raw['x-acs-region-id']
        pop_headers['x-acs-access-key-id'] = raw['x-acs-access-key-id']
        pop_headers['x-acs-signature-method'] = raw['x-acs-signature-method']
        pop_headers['x-acs-signature-nonce'] = raw['x-acs-signature-nonce']
        pop_headers['x-acs-caller-bid'] = '26842'

        raw.update(pop_headers)
        return raw

    def wrapper(*args, **kwargs):
        # `self` must be a `Api` object.
        self = args[0]
        raw_headers = raw_header_func(*args, **kwargs)
        if hasattr(self, 'pop_mock_needed') and self.pop_mock_needed():
            ret = mock_pop(raw_headers)
        else:
            ret = raw_headers
        return ret
    return wrapper
