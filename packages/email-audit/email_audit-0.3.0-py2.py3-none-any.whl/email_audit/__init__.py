# -*- coding: utf-8 -*-

__author__ = 'Johannes Ahlmann'
__email__ = 'johannes@fluquid.com'
__version__ = '0.3.0'

"""
audit whether spam bots are able to extract your email addresses from your
    websites
"""

import re
from six.moves.urllib.parse import unquote

from html_to_etree import parse_html_unicode, parse_html_bytes
from html_text import extract_text
import js2py
from lxml import etree

import six
if six.PY2:
    from HTMLParser import HTMLParser
else:
    from html.parser import HTMLParser


HTML_PARSER = HTMLParser()

"""
sources:
- http://stackoverflow.com/a/38787343
- http://stackoverflow.com/a/2049510
"""
EMAIL_RE = re.compile(
    r"""[\w!#$%&\'*+\-/=?^_`{|}~\.]
        {1,}
        @
        [\w\-\.]
        {1,}
        \.
        \w{2,}
    """,
    flags=re.UNICODE | re.VERBOSE)

MAILTO_RE = re.compile(
    r'^mailto:(.*)', flags=re.U)

AT_DOT_RE = re.compile(
    r"""
    [\w!#$%&\'*+\-/=?^_`{|}~\.]{1,}
    \ ?
    (?:at|\[at\]|\(at\))
    \ ?
    [\w\-\.]{1,}
    \ ?
    (?:dot|\[dot\]|\(dot\))
    \ ?
    \w{2,}
    """,
    flags=re.UNICODE | re.VERBOSE | re.I)

X_A_HREF = etree.XPath('//a[@href]')
CF_EMAIL = etree.XPath('//*[@data-cfemail]')

# taken directly from cloudflare enabled sites and wrapped as a function
# TODO: with minimal DOM simulation, could use script as is...
cflare = js2py.eval_js(
    'function(a) {'

    """for(e='',r='0x'+a.substr(0,2)|0,n=2;a.length-n;n+=2)
         e+='%'+('0'+('0x'+a.substr(n,2)^r).toString(16)).slice(-2);"""

    'return e }'
)


def audit_text(text):
    """ look for email addresses in plain unicode text """
    # FIXME: performance? counter-indications?
    text = HTML_PARSER.unescape(unquote(text))

    for match in EMAIL_RE.finditer(text):
        # NOTE: alternatively unescape/unquote whole text?
        yield match.group(0)

    for match in AT_DOT_RE.finditer(text):
        res = match.group(0)
        # prevent matching on lower-case 'at', 'dot'
        # FIXME: better way in regex?
        if not (' at ' in res and ' dot ' in res):
            yield res


def audit_etree(tree):
    """
    look for email addresses in html DOM as well as text generated from DOM
    """
    # FIXME: pre-compile xpath queries
    for tag in CF_EMAIL(tree):
        cfemail = tag.get('data-cfemail')
        if cfemail:
            yield unquote(cflare(cfemail))

    for a_tag in X_A_HREF(tree):
        href = a_tag.get('href')
        unesc = HTML_PARSER.unescape(unquote(href))
        match = MAILTO_RE.search(unesc)
        if match:
            yield match.group(1)

        cfemail = a_tag.get('data-cfemail')
        if cfemail:
            yield unquote(cflare(cfemail))

    text = extract_text(tree)
    for item in audit_text(text):
        yield item


def audit_html_unicode(body):
    """ audit html with given unicode html body """
    tree = parse_html_unicode(body)
    return audit_etree(tree)


def audit_html_bytes(body, content_type=''):
    """ audit html with given bytestring body and header content_type """
    tree = parse_html_bytes(body, content_type)
    return audit_etree(tree)
