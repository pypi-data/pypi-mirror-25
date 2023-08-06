rsanic
==========

Micro framework built on top of sanic.py written in Python 3.

Installing rsanic
=====================

.. code-block:: bash

    pip3 install rsanic

Example app:

* Local Redis service must be installed and running at port 6397

* Shows how to use html or json responses

.. code-block:: bash

    git clone https://github.com/reformo/rsanic.git
    cd rsanic/example
    python3 server.py

or if you have `pm2 <http://pm2.keymetrics.io>`_ installed

.. code-block:: bash

    git clone https://github.com/reformo/rsanic.git
    cd rsanic/example
    pm2 start process.yml

Then use any web browser to open address: http://127.0.0.1:8000/ or  http://127.0.0.1:8000/api or http://127.0.0.1:8000/public/data.json for static file access.

Notes
=====

* rsanic will not follow the `semantic versioning scheme <http://semver.org/>`_ until the version 1.0.0. So there may be BC breaks.


Credits
=======

* `Mehmet Korkmaz <http://github.com/mkorkmaz>`_

Change Log
==========


New in version 0.4.0
--------------------
* Workers added as an option
* Markdown support added


New in version 0.3.1
--------------------
* Container removed


New in version 0.3.0
--------------------
* HTML theming support added
* Access log option added
* Static files support added
* Starting to support to get loop outer codebase
* Controller invoke methods, application_global and controller_global methods changed to async methods

New in version 0.2.2
--------------------
* Autoescape option set True for Jinja to prevent XSS attacks.
* Example pm2 config added

New in version 0.2.1
--------------------
* Requirements updated

New in version 0.2.0
--------------------
* Dependency Injection Container introduced to be used in Rsanic and Applications
* Request injected in to App
* Working example added

New in version 0.1.0
--------------------
* Introduced "rsanic" #WIP


