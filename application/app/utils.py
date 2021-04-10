from loguru import logger


def postgres_test(name, host, user, pswd):
    from psycopg2 import connect, Error
    try:
        conn = connect(f"dbname='{name}' user='{user}' host='{host}' password='{pswd}' connect_timeout=1")
        conn.close()
        return True
    except Error:
        logger.warning("No db connection!")
        return False