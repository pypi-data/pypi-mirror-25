|Build Status|
|Code Coverage|
|Code Health|

python-otopi-mdp
================

otopi Machine Dialog Parser for python

This module allows you automate installation process based on
`otopi <https://github.com/oVirt/otopi>`__ installator.

Requirements
============

.. code::

  six
  otopi

**WARNING**: The otopi package is not hosted on PyPi site, so it couldn't
be included as dependency of this package. It is maintaned by oVirt community,
they ship this module for several package managements.

Usage
=====

1. Set otopi environment to enable machine dialect

.. code::

  DIALOG/dialect=str:machine

2. Spawn desired installer and pass stdin and stdout to parser

3. Process all otopi events in the loop

Example for oVirt Hosted Engine
-------------------------------

.. code:: python

    import subprocess
    import otopimdp as mdp

    # 1. Set machine dialog option
    with open("/etc/ovirt-hosted-engine-setup.env.d/mycustom.env") as fd:
        fd.write(
            'export environment="${environment} DIALOG/dialect=str:machine"\n'
        )

    # 2. Spawn installer
    installer = subprocess.Popen(["hosted-engine", "--deploy"])
    parser = mdp.MachineDialogParser(
        input_=installer.stdout, output=installer.stdin
    )

    # 3. Process events
    while True:
        event = parser.next_event()
        if event is None:
            continue
        event_type = event[mdp.TYPE_KEY]
        if event_type == mdp.TERMINATE_EVENT:
            break

        event_name = event[mdp.ATTRIBUTES_KEY]['name']
        if event_name == "OVEHOSTED_HOST_ID":
            event[mdp.REPLY_KEY] = "1"
        ....
        parser.send_response(event)

Run tests
=========

.. code:: sh

  tox

**NOTE:** For testing purposes, the otopi package is being run from sources.

.. |Build Status| image:: https://travis-ci.org/rhevm-qe-automation/python-otopi-mdp.svg?branch=master
   :target: https://travis-ci.org/rhevm-qe-automation/python-otopi-mdp
.. |Code Coverage| image:: https://codecov.io/gh/rhevm-qe-automation/python-otopi-mdp/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/rhevm-qe-automation/python-otopi-mdp
.. |Code Health| image:: https://landscape.io/github/rhevm-qe-automation/python-otopi-mdp/master/landscape.svg?style=flat
   :target: https://landscape.io/github/rhevm-qe-automation/python-otopi-mdp/master
