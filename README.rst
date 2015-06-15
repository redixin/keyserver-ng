Keyserver NG
************

Key server with email and key validation.

Why?
====

All available keyservers allow to upload any public key without
any validation/confirmaion.

This keyserver sends encrypted email with confirmation link
to public key owner. Public key will be added to database only
if owner retrieve this email, decrypt it, and open confirmaion
link in the browser.

How?
====

Installation
------------

To install in debian based GNU/Linux::

    $ sudo apt-get install python3-pip libgpgme11-dev
    $ sudo pip3 install keyserver-ng

Configuration
-------------

Self documented configuration file can be found in /etc/keyserver-ng.ini

Running
-------

Upstart script::

    $ sudo cp /etc/keyserver-ng/upstart.conf /etc/init/keyserver-ng.conf
    $ sudo service keyserver-ng start

Run in foreground::

    $ sudo keyserver-ng /etc/keyserver-ng/config.ini

Current status
==============

Implemented
-----------

* Upload key/Confirm key
* Fetch key

Not implemented yet
-------------------

* Search key
* Update key
* Sendmail mailer
* Dump DB/Load DB
