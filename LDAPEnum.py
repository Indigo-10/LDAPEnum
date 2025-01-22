import argparse
import ldap3

def create_ldap_connection(username, password, domain, ip_address, unauthenticated, tld):
    server = ldap3.Server(ip_address)
    if unauthenticated:
        connection = ldap3.Connection(server, user=None, password=None, authentication=ldap3.ANONYMOUS)
    else:
        user_dn = f"CN={username},CN=Users,DC={domain},DC={tld}"  
        connection = ldap3.Connection(server, user=user_dn, password=password)
    
    return connection

def search_ldap(connection, search_base):
    connection.search(search_base, '(objectClass=*)', attributes=['sAMAccountName', 'description', 'cn', 'objectSid'])
    return connection.entries

def parse_arguments():
    parser = argparse.ArgumentParser(description="LDAP Query Script")
    parser.add_argument('-u', '--username', help="Username for authenticated bind", required=False)
    parser.add_argument('-p', '--password', help="Password for authenticated bind", required=False)
    parser.add_argument('-n', '--unauthenticated', action='store_true', help="Use unauthenticated bind")
    parser.add_argument('-d', '--domain', help="Domain name", required=True)
    parser.add_argument('-i', '--ip', help="IP address of LDAP server", required=True)
    parser.add_argument('-t', '--tld', help="TLD of the domain", required=True)

    return parser.parse_args()


def main():
    args = parse_arguments()
   
    search_base = f"DC={args.domain},DC={args.tld}" 

    connection = create_ldap_connection(args.username, args.password, args.domain, args.ip, args.unauthenticated, args.tld)

    default = ["Domain Computers", "Cert Publishers", "Domain Users", "Domain Guests", "Group Policy Creator Owners",
     "RAS and IAS Servers", "Allowed RODC Password Replication Group", "Denied RODC Password Replication Group",
    "Enterprise Read-only Domain Controllers", "Cloneable Domain Controllers", "Protected Users", "DnsAdmins", "DnsUpdateProxy"] 

    if connection.bind():
        print("Connection successful")
        entries = search_ldap(connection, search_base)
        
        for entry in entries:
            if entry.sAMAccountName and entry.sAMAccountName not in default:
                print(f"Username: {entry.sAMAccountName}")
                if entry.description:
                    print(f"Description: {entry.description}")
                if entry.cn:
                    print(f"Computer: {entry.cn}")
                if entry.objectSid:
                    print(f"SID: {entry.objectSid}")
                print()
    else:
        print("Failed to bind to the server")

if __name__ == "__main__":
    main()

