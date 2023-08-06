import psycopg2
import traceback
from contextlib import contextmanager


def get_libpq_connection_string_from_url(database_url):
    database_url_sans_protocol = database_url.split('://')[1]
    database_name = database_url_sans_protocol.split('/')[-1]

    has_user = '@' in database_url_sans_protocol
    database_host = database_url_sans_protocol.split('@')[1].split('/')[0] if has_user else database_url_sans_protocol.split('/')[0]

    has_password = ':' in database_url_sans_protocol.split('@')[0]
    database_user = database_url_sans_protocol.split(':')[0] if has_password else database_url_sans_protocol.split('@')[0]
    database_password = database_url_sans_protocol.split(':')[1].split('@')[0] if has_password else None

    libq_connection_string = 'host={host} dbname={name}'.format(host=database_host, name=database_name)
    if has_user:
        libq_connection_string += ' user={}'.format(database_user)
    if has_password:
        libq_connection_string += ' password={}'.format(database_password)
    return libq_connection_string

@contextmanager
def database_connection(database_url):
    DATABASE_CONNECTION_STRING = get_libpq_connection_string_from_url(database_url)
    try:
        with psycopg2.connect(DATABASE_CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                yield cursor
        conn.close()
    except Exception as exception:
        print(traceback.format_exc())
        print('Unable to run query')
        raise exception
