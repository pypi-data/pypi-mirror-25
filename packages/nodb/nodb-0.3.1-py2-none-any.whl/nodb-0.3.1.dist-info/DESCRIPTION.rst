NoDB
====

|Build Status| |Coverage| |PyPI| |Slack| |Gun.io| |Patreon|

*NoDB isn't a database.. but it sort of looks like one!*

**NoDB** an incredibly simple, Pythonic object store based on Amazon's
S3 static file storage.

It's useful for **prototyping**, **casual hacking**, and (maybe) even
low-traffic **server-less backends** for
**`Zappa <https://github.com/Miserlou/Zappa>`__ apps**!

Features
--------

-  Schema-less!
-  Server-less!
-  Uses S3 as a datastore.
-  Loads to native Python objects with ``cPickle``
-  Can use JSON as a serialization format for untrusted data
-  Local filestore based cacheing
-  Cheap(ish)!
-  Fast(ish)! (Especially from Lambda)

Performance
-----------

Initial load test with `Goad <https://goad.io/>`__ of 10,000 requests
(500 concurrent) with a write and subsequent read of the same index
showed an average time of 400ms. This should be more than acceptable for
many applications, even those which don't have sparse data, although
that is preferred.

Installation
------------

**NoDB** can be installed easily via ``pip``, like so:

::

    $ pip install nodb

Warning!
--------

**NoDB** is **insecure by default**! Do not use it for untrusted data
before setting ``serializer`` to ``"json"``!

Usage
-----

**NoDB** is super easy to use!

You simply make a NoDB object, point it to your bucket and tell it what
field you want to index on.

.. code:: python

    from nodb import NoDB

    nodb = NoDB()
    nodb.bucket = "my-s3-bucket"
    nodb.index = "name"

After that, you can save and load literally anything you want, whenever
you want!

.. code:: python

    # Save an object!
    user = {"name": "Jeff", "age": 19}
    nodb.save(user) # True

    # Load our object!
    user = nodb.load("Jeff")
    print user.age # 19

    # Delete our object
    nodb.delete("Jeff") # True

By default, you can save and load any Python object.

Here's the same example, but with a class. Note the import and
configuration is the same!

.. code:: python

    class User(object):
        name = None
        age = None

        def print_name(self):
            print "Hi, I'm " + self.name + "!"

    new_user = User()
    new_user.name = "Jeff"
    new_user.age = 19
    nodb.save(new_user) # True

    jeff = nodb.load("Jeff")
    jeff.print_name() # Hi, I'm Jeff!

Advanced Usage
--------------

Different Serializers
~~~~~~~~~~~~~~~~~~~~~

To use a safer, non-Pickle serializer, just set JSON as your serializer:

.. code:: python

    nodb = NoDB()
    nodb.serializer = "json"

Note that for this to work, your object must be JSON-serializable.

Object Metadata
~~~~~~~~~~~~~~~

You can get metainfo (datetime and UUID) for a given object by passing
``metainfo=True`` to ``load``, like so:

.. code:: python

    # Load our object and metainfo!
    user, datetime, uuid = nodb.load("Jeff", metainfo=True)

You can also pass in a ``default`` argument for non-existent values.

.. code:: python

    user = nodb.load("Jeff", default={}) # {}

Human Readable Indexes
~~~~~~~~~~~~~~~~~~~~~~

By default, the indexes are hashed. If you want to be able to debug
through the AWS console, set ``human_readable_indexes`` to True:

.. code:: python

    nodb.human_readable_indexes = True

Caching
~~~~~~~

You can enable local file caching, which will store previously retrieved
values in the local rather than remote filestore.

.. code:: python

    nodb.cache = True

TODO (Maybe?)
-------------

-  **Tests** with Placebo
-  **Python3** support
-  Local file storage
-  Quering ranges (numberic IDs only), etc.
-  Different serializers
-  Custom serializers
-  Multiple indexes
-  Compression
-  Bucket management
-  Pseudo-locking
-  Performance/load testing

Related Projects
----------------

-  `Zappa <https://github.com/Miserlou/Zappa>`__ - Python's server-less
   framework!
-  `K.E.V. <https://github.com/capless/kev>`__ - a Python ORM for
   key-value stores based on Redis, S3, and a S3/Redis hybrid backend.

Contributing
------------

This project is still young, so there is still plenty to be done.
Contributions are more than welcome!

Please file tickets for discussion before submitting patches. Pull
requests should target ``master`` and should leave NoDB in a "shippable"
state if merged.

If you are adding a non-trivial amount of new code, please include a
functioning test in your PR. For AWS calls, we use the ``placebo``
library, which you can learn to use `in their
README <https://github.com/garnaat/placebo#usage-as-a-decorator>`__. The
test suite will be run by `Travis
CI <https://travis-ci.org/Miserlou/NoDB>`__ once you open a pull
request.

Please include the GitHub issue or pull request URL that has discussion
related to your changes as a comment in the code
(`example <https://github.com/Miserlou/Zappa/blob/fae2925431b820eaedf088a632022e4120a29f89/zappa/zappa.py#L241-L243>`__).
This greatly helps for project maintainability, as it allows us to trace
back use cases and explain decision making.

License
-------

(C) Rich Jones 2017, MIT License.

.. raw:: html

   <p align="center">

.. raw:: html

   </p>

.. |Build Status| image:: https://travis-ci.org/Miserlou/NoDB.svg
   :target: https://travis-ci.org/Miserlou/NoDB
.. |Coverage| image:: https://img.shields.io/coveralls/Miserlou/NoDB.svg
   :target: https://coveralls.io/github/Miserlou/NoDB
.. |PyPI| image:: https://img.shields.io/pypi/v/NoDB.svg
   :target: https://pypi.python.org/pypi/nodb
.. |Slack| image:: https://img.shields.io/badge/chat-slack-ff69b4.svg
   :target: https://slack.zappa.io/
.. |Gun.io| image:: https://img.shields.io/badge/made%20by-gun.io-blue.svg
   :target: https://gun.io/
.. |Patreon| image:: https://img.shields.io/badge/support-patreon-brightgreen.svg
   :target: https://patreon.com/zappa


