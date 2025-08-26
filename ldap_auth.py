from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES

LDAP_SERVER = "ldap://192.168.1.22:389"
BASE_DN = "DC=alaklein,DC=local"

def connect_with_bind_user(bind_dn, bind_password):
    """Authenticate with the bind account DN"""
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=bind_dn, password=bind_password, auto_bind=True)
    print("Bind user authenticated")
    return conn


def get_user_by_sam(conn, samaccountname, attributes=None):
    """
    Search AD for a user by sAMAccountName.
    conn         -> LDAP connection (already bound)
    samaccountname -> username (e.g. jdoe)
    attributes   -> list of attributes to fetch (default: all)
    """
    search_filter = f"(sAMAccountName={samaccountname})"
    conn.search(
        search_base=BASE_DN,
        search_filter=search_filter,
        attributes=attributes or ALL_ATTRIBUTES
    )

    if conn.entries:
        return conn.entries[0]
    else:
        return None


# Example usage:
bind_dn = "CN=ldap bind,OU=PythonAuth,DC=alaklein,DC=local"
bind_password = "S3nh@123"

conn = connect_with_bind_user(bind_dn, bind_password)

# Now fetch multiple users
for username in ["ala.klein"]:
    user_entry = get_user_by_sam(conn, username, attributes=["displayName", "mail", "memberOf"])
    if user_entry:
        print(f"Found {username}: {user_entry.displayName}, {user_entry.mail}, {user_entry.memberOf}")
    else:
        print(f"User {username} not found")
