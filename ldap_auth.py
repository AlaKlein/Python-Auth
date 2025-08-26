from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES
import configparser
import ssl

#Load config attributes
config = configparser.ConfigParser()
config.read("ldap_config")
ldap_server = ""
LDAP_SERVER_IP = config["ldap"]["ldap_server"]
LDAP_PORT = config["ldap"]["ldap_port"]
BASE_DN = config["ldap"]["base_dn"]
BIND_DN = config["ldap"]["bind_dn"]
BIND_PASSWORD = config["ldap"]["bind_password"]
LDAP_ATTRIBUTE_MAPPING = config["ldap"]["ldap_attribute_mapping"]

def connect_with_bind_user():
    global ldap_server
    if int(LDAP_PORT) == 389:
        ldap_server = f"ldap://{LDAP_SERVER_IP}:{LDAP_PORT}"
    elif int(LDAP_PORT) == 636:
        ldap_server = f"ldaps://{LDAP_SERVER_IP}:{LDAP_PORT}"
    print(ldap_server)
    server = Server(ldap_server, get_info=ALL)
    conn = Connection(server, user=BIND_DN, password=BIND_PASSWORD, auto_bind=True)
    print(f"Connected to {ldap_server}")
    return conn

def get_user_by_attribute_mapping(conn, user, attributes=None):
    attribute_mapping_filter = f"({LDAP_ATTRIBUTE_MAPPING}={user})"
    print(attribute_mapping_filter)
    conn.search(
        search_base=BASE_DN,
        search_filter=attribute_mapping_filter,
        attributes=attributes or ALL_ATTRIBUTES
    )
    return conn.entries[0] if conn.entries else None

#main
if __name__ == "__main__":
    user = input("Insert the user info in the {} format:".format(LDAP_ATTRIBUTE_MAPPING))
    conn = connect_with_bind_user()
    user = get_user_by_attribute_mapping(conn, user, attributes=["displayName", "mail", "memberOf"])
if user:
    print("User DN:", user.entry_dn)
    print("Display Name:", user.displayName.value)
    print("Email:", user.mail.value)
else:
    print("User not found")