httpie-f5-auth
===============

`F5Auth <https://github.com/imecimore/httpie-f5-auth>`_ auth plugin for `HTTPie <https://github.com/jkbr/httpie>`_.

Installation
------------

.. code-block:: bash

    $ pip install httpie-api-auth

You should now see ``f5-auth`` under ``--auth-type`` in ``$ http --help`` output.

Usage
-----

.. code-block:: bash

    $ http --auth USER[:PASS] --verify=no --default-scheme=https mybigiq.com/mgmt/shared/echo