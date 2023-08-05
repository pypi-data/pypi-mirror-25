
[![Build Status](https://travis-ci.org/DomWeldon/oopycql.svg?branch=master)](https://travis-ci.org/DomWeldon/oopycql) [![Coverage Status](https://coveralls.io/repos/github/DomWeldon/oopycql/badge.svg?branch=master)](https://coveralls.io/github/DomWeldon/oopycql?branch=master) [![Docs Status](https://readthedocs.org/projects/oopycql/badge/?version=latest)](http://oopycql.rtfd.io)




# OOPyCQL

An object-oriented way to manage Cypher queries in python.

[Full Documentation](http://oopycql.rtfd.io)

## Installation

    pip install oopycql

## QuickStart


Load a query from a file using the same pythonic reference notation you would to load an object.

For example, let's imagine you have an application with a directory structure like the below.

    src/
    ├-controllers/
    │ └-login/
    │   ├-cql/
    │   │ ├─find_user_password_combination.cql
    │   │ └─create_login_event.cql
    |   ├─__init__.py
    |   └─views.py
    ├─__init__.py
    └─app.py


To load a query in ``views.py``, you could use the below:

    from oopycql import CypherQuery

    # relative style import
    cq = CypherQuery('.cql.find_user_password')

    # absolute style import
    cq = CypherQuery('src.controllers.login.cql.create_login_event')


## License

Apache

## Author

Dom Weldon
dom.weldon@gmail.com
