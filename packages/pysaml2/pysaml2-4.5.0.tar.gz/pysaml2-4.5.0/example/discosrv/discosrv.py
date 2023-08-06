import argparse
import importlib
import logging
import mimetypes
import os
import sys

from future.backports.urllib.parse import parse_qs

from saml2 import BINDING_HTTP_REDIRECT
from saml2.attribute_converter import ac_factory
from saml2.discovery import DiscoveryServer
from saml2.extension import mdui
from saml2.httputil import BadRequest, SeeOther, Unauthorized
from saml2.httputil import NotFound
from saml2.httputil import Response
from saml2.mdstore import MetadataStore
from saml2.s_utils import UnknownSystemEntity

logger = logging.getLogger(__name__)


def static_mime(path, environ, start_response):
    logger.info("[static]sending: %s" % (path,))

    # Set content-type based on filename extension
    ext = ""
    i = path.rfind('.')
    if i != -1:
        ext = path[i:].lower()
    content_type = mimetypes.types_map.get(ext, None)

    try:
        if not content_type.startswith('image/'):
            data = open(path, 'r').read()
        else:
            data = open(path, 'rb')
        resp = Response(data, content=content_type)
        return resp(environ, start_response)
    except IOError:
        _dir = os.getcwd()
        resp = NotFound("{} not in {}".format(path, _dir))
    except Exception as err:
        resp = NotFound('{}'.format(err))

    return resp(environ, start_response)


def by_lang(items, lang='en'):
    for item in items:
        if item['lang'] == lang:
            return item['text']
    return ''


def get_idps(mds):
    dres = {}
    _mdui_dn = '{}&{}'.format(mdui.NAMESPACE, 'DisplayName')

    try:
        for entid, item in mds.any2('idp', 'single_sign_on_service',
                                    BINDING_HTTP_REDIRECT).items():
            _name = ''
            try:
                ext_elems = item['extensions']['extension_elements']
            except KeyError:
                pass
            else:
                for elem in ext_elems:
                    if elem['__class__'] == _mdui_dn:
                        _name = elem['text']
                        break

            if not _name:
                try:
                    _name = by_lang(
                        item['organization']['organization_display_name'])
                except KeyError:
                    try:
                        _name = by_lang(
                            item['organization']['organization_name'])
                    except KeyError:
                        _name = entid

            dres[entid] = _name
    except Exception as err:
        return {}

    return dres


class DiscoSrv(object):
    def __init__(self, idps, tlookup, mds, static='static',
                 accept_unauthorized=False):
        self.idps = idps
        self.tlookup = tlookup
        self.static = static
        self.accept_unauthorized = accept_unauthorized
        self.ds = DiscoveryServer()
        self.ds.metadata = mds

    def _static(self, path):
        if path in ["robots.txt", 'favicon.ico']:
            return "{}/robots.txt".format(self.static)
        else:
            for p in ['acs/site/static/', 'site/static/', 'static/', 'export/']:
                if path.startswith(p):
                    return '{}/{}'.format(self.static, path[len(p):])
        return ''

    def application(self, environ, start_response):
        logger.info("Connection from: %s" % environ["REMOTE_ADDR"])
        session = environ['beaker.session']

        path = environ.get('PATH_INFO', '').lstrip('/')
        logger.info("path: %s" % path)

        _path = self._static(path)
        if _path:
            return static_mime(_path, environ, start_response)
        elif path == 'idp':
            dsr = self.ds.parse_discovery_service_request(
                query=environ['QUERY_STRING'])
            try:
                if not self.ds.verify_return(dsr['entityID'], dsr['return']):
                    resp = BadRequest()
                    return resp(environ, start_response)
            except KeyError:
                pass
            except UnknownSystemEntity:
                if not self.accept_unauthorized:
                    resp = Unauthorized()
                    return resp(environ, start_response)

            session['dsr'] = dsr
            resp = Response(mako_template="choice.mako",
                            template_lookup=self.tlookup,
                            headers=[])
            argv = {"idp_list": self.idps}
            return resp(environ, start_response, **argv)
        elif path == 'target':
            _idp = parse_qs(environ['QUERY_STRING'])['idp'][0]
            dsr = session['dsr']
            _url = self.ds.create_discovery_service_response(
                return_url=dsr['return'], entity_id=_idp).encode('utf8')
            resp = SeeOther(_url)
            return resp(environ, start_response)
        else:
            resp = BadRequest()
            return resp(environ, start_response)

if __name__ == '__main__':
    from beaker.middleware import SessionMiddleware
    from cherrypy import wsgiserver
    from mako.lookup import TemplateLookup

    session_opts = {
        'session.type': 'memory',
        'session.cookie_expires': True,
        'session.auto': True,
        'session.timeout': 900
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('-k', dest="insecure", action='store_true')
    parser.add_argument('-m', dest='metadataconf')
    parser.add_argument('-t', dest='template_root', default='./')
    parser.add_argument('-s', dest='static', default='./static')
    parser.add_argument('-p', dest='port')
    parser.add_argument('-T', dest='tls', action='store_true')
    parser.add_argument('-u', dest="accept_unauthorized", action='store_true')
    parser.add_argument(dest="config")
    cargs = parser.parse_args()

    _tr = cargs.template_root
    LOOKUP = TemplateLookup(directories=[_tr + 'templates', _tr + 'htdocs'],
                            module_directory=_tr + 'modules',
                            input_encoding='utf-8',
                            output_encoding='utf-8')

    sys.path.insert(0, '.')
    _conf = importlib.import_module(cargs.config)

    _mdconf = importlib.import_module(cargs.metadataconf)
    acs = ac_factory()
    mds = MetadataStore(acs, None, check_validity=False,
                        disable_ssl_certificate_validation=True)
    mds.imp(_mdconf.METADATA)
    idps = get_idps(mds)
    _app = DiscoSrv(idps, LOOKUP, mds, static=cargs.static,
                    accept_unauthorized=cargs.accept_unauthorized)

    if not cargs.port:
        if cargs.tls:
            _port = 443
        else:
            _port = 80
    else:
        _port = int(cargs.port)

    SRV = wsgiserver.CherryPyWSGIServer(('0.0.0.0', int(_port)),
                                        SessionMiddleware(_app.application,
                                                          session_opts))

    if cargs.tls:
        from cherrypy.wsgiserver.ssl_builtin import BuiltinSSLAdapter

        SRV.ssl_adapter = BuiltinSSLAdapter(_conf.SERVER_CERT, _conf.SERVER_KEY,
                                            _conf.CERT_CHAIN)
        extra = " using SSL/TLS"
    else:
        extra = ""

    txt = "SP listening on port:%s%s" % (_port, extra)
    logger.info(txt)
    print(txt)
    try:
        SRV.start()
    except KeyboardInterrupt:
        SRV.stop()
