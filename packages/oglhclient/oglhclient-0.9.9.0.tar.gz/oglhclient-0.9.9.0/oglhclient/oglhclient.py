#!/usr/bin/python

import os, requests, json, urllib, re, yaml
from collections import namedtuple
from functools import wraps, partial
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode

def ensure_auth(f):
    """
    makes sure the client has a valid token when a function is called
    the call is going to be made once, in case of not authenticated,
    it will try to authenticate and call the function again
    """
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)

        if 'error' in result._asdict() and \
                len(result.error) > 0 and \
                result.error[0].level == 1 and \
                result.error[0].type == 7 and \
                result.error[0].text == 'Invalid session ID':
            args[0]._do_auth()
            return f(*args, **kwargs)
        return result
    return wrapper

class LighthouseApiClient:
    """
    the basic API client, with methods for GET, POST, PUT, and DELETE
    """

    def __init__(self):
        self.url = os.environ.get('OGLH_API_URL')
        self.username = os.environ.get('OGLH_API_USER')
        self.password = os.environ.get('OGLH_API_PASS')

        if not (self.url and self.username and self.password):
            raise RuntimeError("""
            Some of the required environment variables are not set, please refer
            to the documentation: https://github.com/opengear/oglhclient
            """)

        requests.packages.urllib3.disable_warnings()
        self.api_url = self.url + '/api/v1'
        self.token = None
        self.pending_name_ids = {}
        self.s = requests.Session()

        try:
            ramlfile = os.path.join(os.path.dirname(__file__), \
                'og-rest-api-specification-v1.raml')
            with open(ramlfile, 'r') as stream:
                self.raml = yaml.load(re.sub('\\\/','/',re.sub(':\"',': \"',stream.read())))
        except Exception as e:
            r = self.s.get('http://ftp.opengear.com/download/api/lighthouse/og-rest-api-specification-v1.raml')
            self.raml = yaml.load(re.sub('\\\/','/',re.sub(':\"',': \"',r.text)))
        self.raml = self._fix_raml(self.raml)

    def _fix_raml(self, raml):
        """ it fixes some objects that are split like:
        
        /system
        
        /system/time
        
        instead of:
        
        /system
            /time
        it is helpful for parsing the raml file
        """
        top_paths = [p for p in raml.keys() if re.match('^\/', p)]
        for p in top_paths:
            path_parts = p.split('/')
            if len(path_parts) == 3 and ('/' + path_parts[1]) in top_paths:
                raml['/' + path_parts[1]].update({
                    '/' + path_parts[2]: raml[p]
                })
                del raml[p]
            else:
                raml[p] = self._fix_raml(raml[p])
        return raml

    def _headers(self):
        headers = { 'Content-type' : 'application/json' }
        if self.token:
            headers.update({ 'Authorization' : 'Token ' + self.token })
        return headers

    def _do_auth(self):
        data = { 'username' : self.username, 'password' : self.password }
        body = self.post('/sessions', data=data)

        if 'error' in body._asdict():
            raise RuntimeError(body.error.text)

        self.token = body.session

        if not self.token:
            raise RuntimeError('Auth failed')
        self.s.headers = self._headers()

    def _get_api_url(self, path):
        return self.api_url + path

    def _parse_response(self, response):
        try:
            #return json.loads(response.text)
            return json.loads(response.text, \
                object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        except ValueError:
            return response.text

    def _get_url(self, path, **kwargs):
        return self._get_api_url(str.format(path, **kwargs))

    def _get_url_params(self, path, *args, **kwargs):
        for a in args:
            if type(a) is dict:
                kwargs.update(a)
        params = urllib.parse.urlencode({ k: v for k,v in kwargs.items() \
            if not re.match('.*\{' + k + '\}', path) })
        return self._get_url(path, **kwargs), params

    def _apply_ids(self, path, **kwargs):
        """
        in case of kwargs withs ids for objects and/or for parents
        it properly replaces the names
        """
        if len(kwargs) > 0 and not re.match('.*\{id\}$', path):
            child_name = re.sub(r'\{(.*)\}', r'\1', path.split('/')[-1])
            if 'id' in kwargs:
                kwargs[child_name] = kwargs['id']
                del kwargs['id']

            if re.match('.*\{id}', path):
                parent_name = re.sub('s$','',re.sub('ies$','y',path.split('/')[1]))
                if 'parent_id' in kwargs:
                    kwargs['id'] = kwargs['parent_id']
                    del kwargs['parent_id']
                elif parent_name in kwargs:
                    kwargs['id'] = kwargs[parent_name]
                    del kwargs[parent_name]
        return kwargs

    @ensure_auth
    def get(self, path, *args, **kwargs):
        kwargs = self._apply_ids(path, **kwargs)
        url, params = self._get_url_params(path, *args, **kwargs)
        r = self.s.get(url, params=params, verify=False)
        return self._parse_response(r)

    @ensure_auth
    def find(self, path, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            id_name = re.sub(r'\{(.*)\}', r'\1', path.split('/')[-1])
            kwargs = { id_name: args[0] }
            args = []
        elif len(args) == 0:
            kwargs = self._apply_ids(path, **kwargs)

        url, params = self._get_url_params(path, *args, **kwargs)
        r = self.s.get(url, params=params, verify=False)
        return self._parse_response(r)

    @ensure_auth
    def post(self, path, data={}, **kwargs):
        kwargs = self._apply_ids(path, **kwargs)

        if 'data' in kwargs and data == {}:
            data = kwargs['data']
            del kwargs['data']
        url = self._get_url(path, **kwargs)
        r = self.s.post(url, data=json.dumps(data), verify=False)
        return self._parse_response(r)

    @ensure_auth
    def put(self, path, data, **kwargs):
        kwargs = self._apply_ids(path, **kwargs)
        if 'data' in kwargs and data == {}:
            data = kwargs['data']
            del kwargs['data']
        url = self._get_url(path, **kwargs)
        r = self.s.put(url, data=json.dumps(data), verify=False)
        return self._parse_response(r)

    @ensure_auth
    def delete(self, path, **kwargs):
        kwargs = self._apply_ids(path, **kwargs)
        r = self.s.delete(self._get_url(path, **kwargs), verify=False)
        return self._parse_response(r)

    def get_client(self):
        return self._get_client(self.raml, '')

    def _get_client(self, node, path):
        top_children = set([key.split('/')[1] for key in node.keys() \
            if re.match('^\/', key) and len(key.split('/')) == 2])
        sub_children = set(['__'.join(key.split('/')[1:]) for key in node.keys() \
            if re.match('^\/', key) and len(key.split('/')) > 2])
        middle_children = set([s.split('__')[0] for s in sub_children])
        actions = set([key for key in node.keys() if re.match('^[^\/]', key)])

        kwargs = { 'path': path }

        for k in actions:
            if k == 'get' and re.match('.*(I|i)d\}$', path):
                kwargs['find'] = partial(self.find, path)
            elif k == 'get' and \
                (len([l for l in top_children if re.match('\{.+\}', l)]) > 0 \
                or ('description' in node['get'] and \
                re.match('.*(A|a|(T|t)he)\ (l|L)ist\ of', node['get']['description']))):
                kwargs['list'] = partial(self.get, path)
            elif k == 'get':
                kwargs['get'] = partial(self.get, path)
            elif k == 'put':
                kwargs['update'] = partial(self.put, path)
            elif k == 'post':
                kwargs['create'] = partial(self.post, path)
            elif k == 'delete':
                kwargs['delete'] = partial(self.delete, path)
            else:
                kwargs[k] = node[k]

        for k in top_children:
            if re.match('\{.+\}', k):
                inner_props = self._get_client(node['/' + k], path + '/' + k)
                for l in inner_props._asdict():
                    kwargs[l] = inner_props._asdict()[l]
            else:
                kwargs[k] = self._get_client(node['/' + k], path + '/' + k)

        for k in list(middle_children):
            subargs = {}
            if re.match('\{.+\}', k):
                continue
            else:
                for s in [l for l in list(sub_children) if re.match('^' + k, l)]:
                    sub = re.sub('^' + k + '__', '', s)
                    subargs[sub] = self._get_client(node['/' + k + '/' + sub], \
                        path + '/' + k + '/' + sub)
            SubClient = namedtuple('SubClient', ' '.join(subargs.keys()))
            kwargs[k] = SubClient(**subargs)

        SynClient = namedtuple('OgLhClient', ' '.join(kwargs.keys()))
        return SynClient(**kwargs)
