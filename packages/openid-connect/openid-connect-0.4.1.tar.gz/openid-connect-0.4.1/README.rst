openid-connect - Low-level Python OIDC Client library
=====================================================
.. image:: https://badge.fury.io/py/openid-connect.svg
	:target: https://badge.fury.io/py/openid-connect

This is a low-level Python library for authentication against OpenID
Providers (e.g. Google).

For high-level libraries see the Aiakos_ project.

What is OpenID Connect?
-----------------------

It's a OAuth2-based standard for authentication in applications.

Legacy authorization servers
----------------------------

openid-connect does also support some legacy OAuth2 providers
that do not implement OpenID Connect protocol:

- gitlab
- github

Both official and on-premise instances are supported.

Requirements
------------

- Python 2.7 / 3.5+
- python-jose_
- six_

.. _Aiakos: https://gitlab.com/aiakos
.. _python-jose: https://github.com/mpdavis/python-jose
.. _six: https://pypi.python.org/pypi/six/
