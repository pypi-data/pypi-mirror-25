=====================
GYUN Python SDK
=====================

This repository allows you to access `GYUN <https://www.gyun.com>`_
and control your resources from your applications.

This SDK is licensed under
`Apache Licence, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`_.

.. note::
  Requires Python 2.6 or higher, compatible with Python 3,
  for more information please see
  `GYUN SDK Documentation <https://docs.qc.gyun.com/sdk/>`_


------------
Installation
------------

Install via `pip <http://www.pip-installer.org>`_ ::

    $ pip install gyun-sdk

Upgrade to the latest version ::

    $ pip install --upgrade gyun-sdk

Install from source ::

    git clone https://github.com/gyun-gome/gyun-sdk-python.git
    cd gyun-sdk-python
    python setup.py install


---------------
Getting Started
---------------

In order to operate GYUN IaaS or GomeStor (GYUN Object Storage),
you need apply **access key** on `gyun console <https://console.qc.gyun.com>`_ first.


GYUN IaaS API
'''''''''''''''''''
Pass access key id and secret key into method ``connect_to_zone`` to create connection ::

  >>> import gyun.iaas
  >>> conn = gyun.iaas.connect_to_zone(
          'zone id',
          'access key id',
          'secret access key'
      )

The variable ``conn`` is the instance of ``gyun.iaas.connection.APIConnection``,
we can use it to call resource related methods.

Example::

  # launch instances
  >>> ret = conn.run_instances(
          image_id='img-xxxxxxxx',
          cpu=1,
          memory=1024,
          vxnets=['vxnet-0'],
          login_mode='passwd',
          login_passwd='Passw0rd@()'
      )

  # stop instances
  >>> ret = conn.stop_instances(
          instances=['i-xxxxxxxx'],
          force=True
        )

  # describe instances
  >>> ret = conn.describe_instances(
          status=['running', 'stopped']
        )

GYUN GomeStor API
'''''''''''''''''''''''
Pass access key id and secret key into method ``connect`` to create connection ::

  >>> import gyun.gomestor
  >>> conn = gyun.gomestor.connect(
          'pek3a.gomestor.com',
          'access key id',
          'secret access key'
      )

The variable ``conn`` is the instance of ``gyun.gomestor.connection.QSConnection``,
we can use it to create Bucket which is used for generating Key and MultiPartUpload.

Example::

  # Create a bucket
  >>> bucket = conn.create_bucket('mybucket')

  # Create a key
  >>> key = bucket.new_key('myobject')
  >>> with open('/tmp/myfile') as f:
  >>>     key.send_file(f)

  # Delete the key
  >>> bucket.delete_key('myobject')
