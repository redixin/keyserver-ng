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

Changelog
=========

Version 0.1.0
-------------
New features:

* Upload key/Confirm key
* Fetch key

Roadmap
=======

Version 0.2.0
-------------
* Search key
* Update key
* Sendmail mailer

Version 0.3.0
-------------
* MySQL backend
* Dump DB/Load DB

Version 0.4.0
-------------
* Server pools
