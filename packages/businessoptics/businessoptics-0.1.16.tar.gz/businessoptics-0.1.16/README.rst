BusinessOptics Client
---------------------

Easy access to the BusinessOptics API, based on the python requests library.

For example::

    from businessoptics import Client

    print Client(auth=('user@example.com', 'apikey')).workspace(123).query('ideaname').tuples()
