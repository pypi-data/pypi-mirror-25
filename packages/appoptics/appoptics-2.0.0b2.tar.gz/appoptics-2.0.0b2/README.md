# python-appoptics

The 'appoptics' module provides support for instrumenting
programs for use with the AppOptics instrumentation library.

The appoptics module provides a Pythonic interface to liboboe for C, and middleware 
and other components for popular web frameworks such as Django, Tornado, Pyramid, and WSGI.


## Installing

The Python instrumentation for AppOptics uses a module named `appoptics`, which you
can get from pip by running:

```sh
pip install appoptics
```

## Configuring

See our documentation on [configuring AppOptics for python](http://docs.appoptics.com/Instrumentation/python.html#configuring-instrumentation).

# Upgrading

To upgrade an existing installation, you simply need to run:

```sh
pip install appoptics --upgrade
```

## Running the Tests

### Test dependencies

The test suite depends on the presence of several database and cache servers.

- mysql
- postgres
- mongodb
- memcached
- redis

The test suite uses [tox](https://testrun.org/tox/latest/), a tool for running
tests against different versions of python and depended modules. You can get it
from apt by running `sudo apt-get install python-tox` or from pip with
`sudo pip install tox`.

The tests currently run against python 2.6 and 2.7, so you will need both.

To set up multiple versions of python:

    sudo apt-get install python-software-properties software-properties-common
    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python2.6 python2.6-dev

### Configuring test database and cache servers

MySQL SQLAlchemy tests require no-auth TCP connection (as testing user).

PostgreSQL SQLAlchemy tests requires no-auth (trust) TCP connection (as testing user).

```
# in pg_hba.conf: Don't use this in production!!
host    all             all             127.0.0.1/32            trust
```

### Running the tests

To run tests, simply run:

```sh
tox
```

### Test directory layout

Tests in test/unit are actually functional tests; naming is for historic
reasons.  Tests in test/manual are for manual verification of certain
behaviors.

## Support

If you find a bug or would like to request an enhancement, feel free to file
an issue. For all other support requests, please email support@appoptics.com.

## Contributing

You are obviously a person of great sense and intelligence. We happily
appreciate all contributions to the appoptics module whether it is documentation,
a bug fix, new instrumentation for a library or framework or anything else
we haven't thought of.

We welcome you to send us PRs. We also humbly request that any new
instrumentation submissions have corresponding tests that accompany
them. This way we don't break any of your additions when we (and others)
make changes after the fact.

## Developer Resources

We have made a large effort to expose as much technical information
as possible to assist developers wishing to contribute to the AppOptics module.
Below are the three major sources for information and help for developers:

* The [AppOptics Knowledge Base](https://docs.appoptics.com/)
has a large collection of technical articles or, if needed, you can submit a
support request directly to the team.

If you have any questions or ideas, don't hesitate to contact us anytime.

To see the code related to the C++ extension, take a look in `appoptics/swig`.

## License

Copyright (c) 2016 SolarWinds, LLC

Released under the [Librato Open License](http://docs.appoptics.com/Instrumentation/librato-open-license.html)
