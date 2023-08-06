===========
email audit
===========

.. image:: https://img.shields.io/pypi/v/email-audit.svg
        :target: https://pypi.python.org/pypi/email-audit

.. image:: https://img.shields.io/pypi/pyversions/email-audit.svg
        :target: https://pypi.python.org/pypi/email-audit

.. image:: https://img.shields.io/travis/fluquid/email-audit.svg
        :target: https://travis-ci.org/fluquid/email-audit

.. image:: https://codecov.io/github/fluquid/email-audit/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/fluquid/email-audit

.. image:: https://requires.io/github/fluquid/email-audit/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/fluquid/email-audit/requirements/?branch=master

Audit which email addresses can be collected by bots from your sites.

Bot can harvest emails from websites, and many obfuscation techniques are
not as effective as they may seem.
This tool helps you find a good balance between ease-of-use for your users on 
the one side, and thwarting spam bots on the other.

* Free software: MIT license
* Python versions: 2.7, 3.4+

Features
--------

* audit / find emails that spam bots can find on your sites

Quickstart
----------

Generator of detected emails from bytestring html::

    import requests
    from email_audit import audit_html_bytes

    res = requests.get('http://example.co/')
    list(audit_html_bytes(res.content, res.headers.get('content-type')))
    
    ['example@gmail.com', 'info [at] example [dot] co',
     'Jonas.Tullus@президент.рф', '#!$%&'*+-/=?^_`{}|~@example.org']

Generator of found emails from unicode html::

    emails = audit_html_unicode(unicode_body)

Credits
-------

This package was created with Cookiecutter_ and the `fluquid/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`fluquid/cookiecutter-pypackage`: https://github.com/fluquid/cookiecutter-pypackage
