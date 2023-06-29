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

# Nmap scan for open SMTP ports and version detection
print_section_header "Nmap Scan - Open SMTP Ports and Version Detection"
nmap_smtp_command="nmap -p 25,465,587 --script smtp-commands,smtp-vuln*,ssl-cert $TARGET"
echo "Nmap Command:"
echo "$nmap_smtp_command"
eval "$nmap_smtp_command"

echo ""

# SMTP banner grabbing
print_section_header "SMTP Banner Grabbing"
smtp_banner_grabbing_command="nc -vz $TARGET 25"
echo "SMTP Banner:"
eval "$smtp_banner_grabbing_command"

echo ""

# SMTP enumeration
print_section_header "SMTP Enumeration"
smtp_enum_command="smtp-user-enum -M VRFY -U users.txt -t $TARGET"
echo "SMTP Enumeration:"
eval "$smtp_enum_command"

echo ""

# Email spoofing
print_section_header "Email Spoofing"
email_spoofing_command="sendemail -f sender@example.com -t recipient@example.com -u 'Test Email' -m 'This is a test email.' -s $TARGET:25"
echo "Email Spoofing:"
eval "$email_spoofing_command"

echo ""

# SMTP security misconfigurations
print_section_header "SMTP Security Misconfigurations"
smtp_check_relay_command="smtp-check -r $TARGET"
echo "SMTP Open Relay Check:"
eval "$smtp_check_relay_command"

smtp_check_expn_command="smtp-check -e $TARGET"
echo "SMTP EXPN Check:"
eval "$smtp_check_expn_command"

smtp_check_vrfy_command="smtp-check -v $TARGET"
echo "SMTP VRFY Check:"
eval "$smtp_check_vrfy_command"

echo ""

# SMTP user enumeration and bruteforcing
print_section_header "SMTP User Enumeration and Bruteforcing"
smtp_user_enum_command="smtp-user-enum -M RCPT -U users.txt -t $TARGET"
echo "SMTP User Enumeration:"
eval "$smtp_user_enum_command"

smtp_user_bruteforce_command="smtp-user-enum -M RCPT -U users.txt -p passwords.txt -t $TARGET"
echo "SMTP User Bruteforce:"
eval "$smtp_user_bruteforce_command"

echo ""

# SMTP service discovery
print_section_header "SMTP Service Discovery"
smtp_service_discovery_command="smtp-enum-users -M VRFY -u users.txt -t $TARGET"
echo "SMTP Service Discovery:"
eval "$smtp_service_discovery_command"

echo ""

echo "SMTP Recon completed."
