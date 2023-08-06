# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from email_audit import (audit_etree, audit_text, audit_html_unicode,
                         audit_html_bytes)
from html_text import parse_html


def split_text(text):
    return [x for x in text.split('\n') if x.strip()]


def test_cfemail():
    MAILTO = """
<a href="/cdn-cgi/l/email-protection#e48d8a828ba496819091968ac98b8ac98d8a978d838c90ca878b89"><span class="__cf_email__" data-cfemail="cfa6a1a9a08fbdaabbbabda1e2a0a1e2a6a1bca6a8a7bbe1aca0a2">[email&#160;protected]</span></a>
<a href="/cdn-cgi/l/email-protection#761f1810193602121711041903065815191b"><span class="__cf_email__" data-cfemail="a2cbccc4cde2d6c6c3c5d0cdd7d28cc1cdcf">[email&#160;protected]</span></a>
<a href="/cdn-cgi/l/email-protection#7b131e1717143b081e091e151f120b120f024955181416"><span class="__cf_email__" data-cfemail="a5cdc0c9c9cae5d6c0d7c0cbc1ccd5ccd1dc978bc6cac8">[email&#160;protected]</span></a>
<a class='underline' href="/cdn-cgi/l/email-protection#452c2b232a052824372e2031373c2c2b266b262a28"><span class="__cf_email__" data-cfemail="a3cacdc5cce3cec2d1c8c6d7d1dacacdc08dc0ccce">[email&#160;protected]</span></a>
    """
    for sample in split_text(MAILTO):
        tree = parse_html(sample)
        res = list(set(audit_etree(tree)))
        assert len(res) == 1 and '@' in res[0], (sample, res)


def test_etree_mailto():
    MAILTO = """
<a href="mailto:foo@bar.baz">
<a href="mailto:%66%6f%6f%40%62%61%72%2e%63%6f%6d">
<a href="mailto:silvan3&#64;tilllate&#46;com">
<a href="mailto:%73%69%6c%76%61%6e%34%40%74%69%6c%6c%6c%61%74%65%2e%63%6f%6d">
<a href="mailto:%75%73%65%72%40%64%6f%6d%61%69%6e%2e%74%6c%64">
<a href="&#109&#97&#105&#108&#116&#111&#58&#117&#115&#101&#114&#64&#100&#111&#109&#97&#105&#110&#46&#116&#108&#100">
<a href='m&#97;ilto&#58;%4Aoh&#110;&#46;Doe&#64;e%78a&#109;&#112;le%2E%63&#111;m'>
<a href='&#109;&#97;&#105;&#108;&#116;&#111;&#58;&#106;&#111;&#104;&#110;&#64;&#121;&#97;&#104;&#111;&#111;&#46;&#99;&#111;&#109;'>
    """
    for sample in split_text(MAILTO):
        tree = parse_html(sample)
        res = list(audit_etree(tree))
        assert len(res) == 1 and '@' in res[0], (sample, res)


def test_text_plain():
    VALID = """
武@メール.グーグル
jonas@Bücher.de
me@ge.jobs
Jonas.Tullus@президент.рф
Jonas_Tullus-Meyer@googlemail.com
prettyandsimple@example.com
very.common@example.com
disposable.style.email.with+symbol@example.com
other.email-with-dash@example.com
x@example.com
example-indeed@strange-example.com
#!$%&'*+-/=?^_`{}|~@example.org
example@s.solutions
xyz&#64;example&#46;com
xyz%40example.com
J&#111;hn&#46;Do&#101;&#64;&#101;xa&#109;ple&#46;co&#109;
&#106;&#111;&#104;&#110;&#64;&#121;&#97;&#104;&#111;&#111;&#46;&#99;&#111;&#109;
    """

    INVALID = """
@twitter_handle
    """

    for valid in split_text(VALID):
        res = list(audit_text(valid))
        assert len(res) == 1 and '@' in res[0], (valid, res)

    for invalid in split_text(INVALID):
        res = list(audit_text(invalid))
        assert len(res) == 0, (invalid, res)


def test_at_dot():
    VALID = """
user [at] domain [dot] tld
foo AT bar DOT baz
jt.superuser[AT]gmail[DOT]com
contact(at)company(dot)com
    """
# info(at)embeemobile.com

    INVALID = """
he arrived at the dot exactly.
    """

    for at_dot in split_text(VALID):
        res = list(audit_text(at_dot))
        assert len(res) == 1, (at_dot, res)

    for at_dot in split_text(INVALID):
        res = list(audit_text(at_dot))
        assert len(res) == 0, (at_dot, res)


def test_tags():
    # FIXME: this one is tricky re: whitespace handling
    #   `no-one<i>@</i>example<i>.</i>com`
    #
    #   `<span>Email:</span>a@b.c` vs.
    #   `<span>a</span>@<span>b</span>.<span>c</span>`

    HTMLS = """
foo<!-- >@. -->@<!-- >@. -->bar<!-- >@. -->.<!-- >@. -->baz
user<!-- pre @ -->@<!--- post @ -->do<!-- post first syllable -->main<!--- pre dot -->.tld
silvan5<!-- -->@<!--- @ -->till<!-- -->late.<!--- . -->com
    """
    for html in split_text(HTMLS):
        res = list(audit_html_unicode(html))
        assert len(res) == 1, (html, res)


def test_bytes():
    body = """
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  </head>
  <body>
    <a href="mailto:john@yahoo.com">john@yahoo.com</a>
  </body>
</html>
    """
    res = list(audit_html_bytes(body.encode('utf-8')))
    assert len(res) == 2 and res[0] == res[1], (body, res)


def test_cloudflare():
    CF_DATA = """
    <a class="__cf_email__" href="/cdn-cgi/l/email-protection"
    data-cfemail="5c32392b3a352832392f2f3f331c3b313d3530723f3331">
    """
    TARGET = "newfitnessco@gmail.com"
    res = list(set(audit_html_unicode(CF_DATA)))
    assert len(res) == 1 and TARGET == res[0], res
