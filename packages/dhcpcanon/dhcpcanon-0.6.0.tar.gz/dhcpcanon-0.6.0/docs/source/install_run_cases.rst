system files
-------------

sbin/dhcpcanon-script (might need different path)
systemd/dhcpcanon.service
tmpfiles.d/dhcpcanon.conf
console_scripts ->  /usr/bin/dhcpcanon

run cases
----------

* standalone without systemd
* with Gnome // // with Network Manager
* with wrapper
* with systemd
* with systemd from debian package
* with debian package without systemd?

install cases
--------------

* standalone without systemd
* with wrapper
* with systemd
* with Gnome Network Manager

* temporal with systemd?

install from
-------------

* setup.py
* pip
* install script
* Debian

standalone without systemd
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

paths to install could be in:

virtualenv
^^^^^^^^^^^

installed by command::

    pip install -e .

or::

    python setup.py develop

resulting pahts,
- /home/user/.virtualenvs/dhcpcanonuser3env/

these doesn't make sense:
- /home/user/.virtualenvs/dhcpcanonuser3env/lib/systemd/system/dhcpcanon.service
- /home/user/.virtualenvs/dhcpcanonuser3env/run/tmpfiles.d/dhcpcanon.conf
- /home/user/.virtualenvs/dhcpcanonuser3env/sbin/dhcpcanon-script

--user
^^^^^^^

installed by command::

    python setup.py install --user

resulting paths:
- /home/user/.local/lib/python3.5/site-packages/

these doesn't make sense?

--prefix
^^^^^^^^^

installed by command::

    python setup.py install --prefix

sudo
^^^^^^^^^^^^^^

installed by command::

    sudo python setup.py install

pip
^^^^^^


temporal
^^^^^^^^^

- /run/systemd/system/dhcpcanon.service
- /run/tmpfiles.d/dhcpcanon.conf
- /sbin/dhcpcanon-script

debian (permanent)
^^^^^^^^^^^^^^^^^^^

- /lib/systemd/system/dhcpcanon.service
- /usr/lib/tmpfiles.d/dhcpcanon.conf
- /sbin/dhcpcanon-script
- /usr/bin/dhcpcanon
