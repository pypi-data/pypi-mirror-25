# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1463586213.197051
_enable_loop = True
_template_filename = 'htdocs/choice.mako'
_template_uri = 'choice.mako'
_source_encoding = 'utf-8'
_exports = []



def idp_choice(idp_list):
    """
    Creates a drop down list of IdPs
    :param idp_list: dictionary of entities, keys are entity_id's
        values are human readable names.
    """
    l = idp_list.keys()
    l.sort()
    element = "<select name=\"idp\">"
    for i in l:
        element += "<option value=\"%s\">%s</option>" % (i, idp_list[i])
    element += "</select>"
    return element


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        idp_list = context.get('idp_list', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n<!DOCTYPE html>\n\n<html>\n  <head>\n    <title>SAML2 Discovery Service</title>\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <!-- Bootstrap -->\n    <link href="static/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">\n      <link href="static/style.css" rel="stylesheet" media="all">\n\n    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->\n    <!--[if lt IE 9]>\n      <script src="../../assets/js/html5shiv.js"></script>\n      <script src="../../assets/js/respond.min.js"></script>\n    <![endif]-->\n  </head>\n  <body>\n\n    <!-- Static navbar -->\n    <div class="navbar navbar-default navbar-fixed-top">\n        <div class="navbar-header">\n          <a class="navbar-brand" href="#">pyoidc RP</a>\n        </div>\n    </div>\n\n    <div class="container">\n     <!-- Main component for a primary marketing message or call to action -->\n      <div class="jumbotron">\n        <form class="form-signin" action="target" method="get">\n        <h1>IdP choice</h1>\n          <h3>Chose the IdP from this list: </h3>\n            ')
        __M_writer(unicode(idp_choice(idp_list)))
        __M_writer(u'\n            <button class="btn btn-lg btn-primary btn-block" type="submit">Start</button>\n        </form>\n      </div>\n\n    </div> <!-- /container -->\n    <!-- jQuery (necessary for Bootstrap\'s JavaScript plugins) -->\n    <script src="/static/jquery.min.1.9.1.js"></script>\n    <!-- Include all compiled plugins (below), or include individual files as needed -->\n    <script src="/static/bootstrap/js/bootstrap.min.js"></script>\n  </body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"32": 0, "38": 15, "39": 48, "40": 48, "46": 40, "16": 1}, "uri": "choice.mako", "filename": "htdocs/choice.mako"}
__M_END_METADATA
"""
