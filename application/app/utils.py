
def postgres_test(name, user, host, pswd):
    from psycopg2 import connect, Error
    try:
        conn = connect(f"dbname='{name}' user='{user}' host='{host}' password='{pswd}' connect_timeout=1")
        conn.close()
        return True
    except Error:
        return False