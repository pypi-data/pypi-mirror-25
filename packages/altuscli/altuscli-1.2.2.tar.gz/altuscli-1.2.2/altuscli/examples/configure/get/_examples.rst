Suppose you had the following config file::

    [default]
    altus_access_key_id=default_access_key
    altus_private_key=default_private_key

    [foobar]
    farboo=true

    [profile testing]
    altus_access_key_id=testing_access_key
    altus_private_key=testing_private_key

The following commands would have the corresponding output::

    $ altus configure get altus_access_key_id
    default_access_key

    $ altus configure get default.altus_access_key_id
    default_access_key

    $ altus configure get altus_access_key_id --profile testing
    testing_access_key

    $ altus configure get profile.testing.altus_access_key_id
    testing_access_key

    $ altus configure get foobar.farboo
    true

    $ altus configure get preview.does-not-exist
    $
    $ echo $?
    1
