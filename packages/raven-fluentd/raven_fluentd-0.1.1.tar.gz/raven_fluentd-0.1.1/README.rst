========================
Raven Transports Fluentd
========================


.. image:: https://img.shields.io/pypi/v/raven-fluentd.svg
        :target: https://pypi.python.org/pypi/raven-fluentd

.. image:: https://img.shields.io/travis/ayemos/raven-transports-fluentd-python.svg
        :target: https://travis-ci.org/ayemos/raven-transports-fluentd-python

.. image:: https://readthedocs.org/projects/raven-transports-fluentd-python/badge/?version=latest
        :target: https://raven-transports-fluentd-python.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/ayemos/raven-transports-fluentd-python/shield.svg
     :target: https://pyup.io/repos/github/ayemos/raven-transports-fluentd-python/
     :alt: Updates


A transport for raven-python which supports fluentd.


* Free software: MIT license
* Documentation: https://raven-transports-fluentd.readthedocs.io.


Installation
------------

Install via pip::

  pip install raven-transports-fluentd

or from source::

  $ git clone https://github.com/ayemos/raven-transports-fluentd raven-transports-fluentd
  $ cd raven-transports-fluentd
  $ python setup.py install


Usage
-----

.. code:: python

  import os

  from raven import Client
  from raven_fluentd.transport import FluentdTransport


  def main():
      sentry_public_key = os.environ['SENTRY_PUBLIC_KEY']
      sentry_secret_key = os.environ['SENTRY_SECRET_KEY']
      sentry_project_id = os.environ['SENTRY_PROJECT_ID']
      dsn = 'fluentd://%(sentry_public_key)s:%(sentry_secret_key)s@fluentd:24224/%(sentry_project_id)s' \
            % locals()

      client = Client(dsn, transport=FluentdTransport)

      try:
          1 / 0
      except ZeroDivisionError:
          client.captureException()


  if __name__ == '__main__':
      main()



See `./docker_test` for more detail (the test example comes with working fluent.conf).


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

