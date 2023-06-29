#!/bin/bash

# Check if the target IP address or hostname argument is provided
if [ $# -lt 1 ]; then
    echo "Please provide a target IP address or hostname as a command-line argument."
    exit 1
fi

# Define the target IP address or hostname
TARGET="$1"

# Function to print section headers
print_section_header() {
    echo "------------------------------------"
    echo "$1"
    echo "------------------------------------"
}

# Nmap scan for open Zimbra ports and version detection
print_section_header "Nmap Scan - Open Zimbra Ports and Version Detection"
nmap_zimbra_command="nmap -p 25,110,143,465,587,993,995 $TARGET"
echo "Nmap Command:"
echo "$nmap_zimbra_command"
eval "$nmap_zimbra_command"

echo ""

# Zimbra version detection
print_section_header "Zimbra Version Detection"
zimbra_version_command="nc -vz $TARGET 25"
echo "Zimbra Version:"
eval "$zimbra_version_command"

echo ""

# Zimbra enumeration
print_section_header "Zimbra Enumeration"
zimbra_enum_command="nc -vz $TARGET 110 && nc -vz $TARGET 143 && nc -vz $TARGET 465 && nc -vz $TARGET 587 && nc -vz $TARGET 993 && nc -vz $TARGET 995"
echo "Zimbra Enumeration:"
eval "$zimbra_enum_command"

echo ""

# Zimbra username enumeration
print_section_header "Zimbra Username Enumeration"
zimbra_enum_users_command="hydra -L users.txt -P passwords.txt $TARGET pop3 imap -t 4 -V"
echo "Zimbra Username Enumeration:"
eval "$zimbra_enum_users_command"

echo ""

# Zimbra password spraying
print_section_header "Zimbra Password Spraying"
zimbra_spray_command="hydra -L users.txt -P passwords.txt $TARGET smtp -t 4 -V"
echo "Zimbra Password Spraying:"
eval "$zimbra_spray_command"

echo ""

# Zimbra mail relay check
print_section_header "Zimbra Mail Relay Check"
zimbra_relay_check_command="smtp-user-enum -M VRFY -U users.txt -t $TARGET"
echo "Zimbra Mail Relay Check:"
eval "$zimbra_relay_check_command"

echo ""

# Zimbra mailbox enumeration
print_section_header "Zimbra Mailbox Enumeration"
zimbra_mailbox_enum_command="nmap --script imap-capabilities -p 143 $TARGET"
echo "Zimbra Mailbox Enumeration:"
eval "$zimbra_mailbox_enum_command"

echo ""

# Zimbra web interface enumeration
print_section_header "Zimbra Web Interface Enumeration"
zimbra_web_enum_command="dirb http://$TARGET /usr/share/dirb/wordlists/common.txt"
echo "Zimbra Web Interface Enumeration:"
eval "$zimbra_web_enum_command"

echo ""

echo "Zimbra Recon completed."
