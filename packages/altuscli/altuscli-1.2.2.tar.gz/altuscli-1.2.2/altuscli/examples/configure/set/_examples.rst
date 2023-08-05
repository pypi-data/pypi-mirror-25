Given an empty config file, the following commands::

    $ altus configure set altus_access_key_id default_access_key
    $ altus configure set altus_private_key default_private_key
    $ altus configure set default.ca_bundle /path/to/ca-bundle.pem
    $ altus configure set foobar.farboo.true

will produce the following config file::

    [default]
    ca_bundle = /path/to/ca-bundle.pem

    [foobar]
    farboo = true

and the following ``~/.altus/credentials`` file::

    [default]
    altus_access_key_id = default_access_key
    altus_private_key = default_private_key
