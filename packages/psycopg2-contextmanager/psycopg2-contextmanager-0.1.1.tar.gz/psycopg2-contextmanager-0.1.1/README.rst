Installation
============

Run ``pip install git+ssh://git@bitbucket.org/GRIDSMART/gsdb.git``

Usage
=====

::

    from gsdb import database_connection

    with database_connection(<database_connection_string>) as cursor:
        cursor.execute(<query>)

Commits are handled automatically. If the query fails, the package will log the exception along with the line ``Unable to run query`` and re-raise it.
