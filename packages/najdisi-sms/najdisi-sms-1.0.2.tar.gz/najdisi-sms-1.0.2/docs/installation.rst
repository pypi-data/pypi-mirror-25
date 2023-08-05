Installation
++++++++++++

From pypi
---------

You need the python-pip package and super user access to install system wide::

  pip install najdisi-sms

You can also install the package in virtualenv::

  virtualenv venv
  source venv/bin/activate
  pip install najdisi-sms

The CLI command can be found in "venv/bin/najdisi-sms" and you can add it to you PATH or call it directly.


From source
-----------

You can install the package systemwide with (you need su access)::

  make install
  #or
  pip install .

If you dont want/have super user access, you can install it in a python virtual env
in the root folder call::

  virtualenv venv
  source venv/bin/activate
  pip install .

The CLI command can be found in "venv/bin/najdisi-sms" and you can add it to you PATH or call it directly.
