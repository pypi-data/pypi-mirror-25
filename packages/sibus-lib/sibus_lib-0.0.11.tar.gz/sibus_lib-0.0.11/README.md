SiBus Lib - Library for creating SiBus clients and servers
========================================================

Vous pouvez l'installer avec pip:

    sudo apt-get install mariadb-client-10.0
    sudo apt-get install mariadb-server-10.0

    sudo mysql -u root
    >>> CREATE DATABASE sibus_database;
    >>> GRANT ALL ON sibus_database.* TO alex@localhost IDENTIFIED BY 'alpi';
    >>> \q

    pip install zmq PyYaml marshmallow sqlalchemy sqlalchemy_utils PyMySQL python-dateutil
    pip install sibus_lib

Exemple d'usage:

    >>> from sibus_lib import sibus_init
    >>> from sibus_lib import BusCore

    >>> logger, cfg_data = sibus_init("bus.core")
    >>> buscore = BusCore()
    >>> buscore.start()

Ce code est sous licence WTFPL.
