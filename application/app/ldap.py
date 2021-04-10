import ldap
import os

from loguru import logger

from .db import db, User


def init(app): 
    ldapuri = os.environ.get("LDAPURI")
    ldapbase = os.environ.get("LDAPBASE")
    ldapbind = os.environ.get("LDAPBIND")
    ldappswd = os.environ.get("LDAPPSWD")

    ldap_conn = ldap.initialize(ldapuri)
    ldap_conn.simple_bind_s(ldapbind, ldappswd)

    searchFilter = "(objectClass=*)"
    searchAttribute = ["givenname","sn"]
    searchScope = ldap.SCOPE_SUBTREE

    try:
        ldaprslt = ldap_conn.search(ldapbase, searchScope, searchFilter, searchAttribute)
        result_set = []
        while 1:
            result_type, result_data = ldap_conn.result(ldaprslt, 0)
            if (result_data == []):
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
        print(result_set)
        for entry in result_set[1:]:
            logger.success(entry)
            user = User(first_name=entry[0][1]["givenName"][0].decode("utf-8"), mid_name="", last_name=entry[0][1]["sn"][0].decode("utf-8"))
            with app.app_context():
                db.session.add(user)
                db.session.commit()
    except ldap.LDAPError as e:
        import traceback
        traceback.print_tb(e)
