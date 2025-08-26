from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES
import configparser

#Load config attributes
config = configparser.ConfigParser()
config.read("ldap_config")
LDAP_SERVER_IP = config["ldap"]["ldap_server"]
LDAP_PORT = config["ldap"]["ldap_port"]
LDAP_SERVER = f"ldap://{LDAP_SERVER_IP}:{LDAP_PORT}"
BASE_DN = config["ldap"]["base_dn"]
BIND_DN = config["ldap"]["bind_dn"]
BIND_PASSWORD = config["ldap"]["bind_password"]
LDAP_ATTRIBUTE_MAPPING = config["ldap"]["ldap_attribute_mapping"]

def connect_with_bind_user():
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=BIND_DN, password=BIND_PASSWORD, auto_bind=True)
    print(f"Connected to {LDAP_SERVER}")
    return conn

def get_user_by_sam(conn, attribute_mapping, attributes=None):
    if LDAP_ATTRIBUTE_MAPPING == "sAMAccountName":
        search_filter = f"(sAMAccountName={attribute_mapping})"
    elif LDAP_ATTRIBUTE_MAPPING == "userPrincipalName":
        search_filter = f"(userPrincipalName={attribute_mapping})"
    print(search_filter)
    conn.search(
        search_base=BASE_DN,
        search_filter=search_filter,
        attributes=attributes or ALL_ATTRIBUTES
    )
    return conn.entries[0] if conn.entries else None

#main
if __name__ == "__main__":
    user = input("Insert the user info in the {} format:".format(LDAP_ATTRIBUTE_MAPPING))
    conn = connect_with_bind_user()
    user = get_user_by_sam(conn, user, attributes=["displayName", "mail", "memberOf"])
    if user:
        print("User found:", user)
    else:
        print("User not found")