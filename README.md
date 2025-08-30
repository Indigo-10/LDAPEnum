# LDAPEnum

Simple LDAP enumeration script for Active Directory environments. Connects to LDAP servers and extracts basic user information while filtering out default domain groups.

## What it does

- Connects to LDAP servers (authenticated or anonymous)
- Queries for objects with sAMAccountName, description, cn, and objectSid attributes
- Filters out default Windows domain groups to focus on custom users/computers
- Displays usernames, descriptions, computer names, and SIDs

## Usage

```bash
# Authenticated bind
python3 LDAPEnum.py -u username -p password -d domain -i 10.0.0.1 -t com

# Anonymous bind
python3 LDAPEnum.py -n -d domain -i 10.0.0.1 -t com
```

## Output

For each non-default object found, displays:
- Username (sAMAccountName)
- Description field (often contains useful info)
- Computer name (cn)
- Security Identifier (objectSid)

---
*Built for authorized security testing and research purposes*
