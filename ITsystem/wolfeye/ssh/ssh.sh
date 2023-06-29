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

# Nmap scan for open SSH ports and version detection
print_section_header "Nmap Scan - Open SSH Ports and Version Detection"
nmap_ssh_command="nmap -p 22 --script ssh* $TARGET"
echo "Nmap Command:"
echo "$nmap_ssh_command"
eval "$nmap_ssh_command"

echo ""

# SSH banner grabbing
print_section_header "SSH Banner Grabbing"
ssh_banner_grabbing_command="nc -vz $TARGET 22"
echo "SSH Banner:"
eval "$ssh_banner_grabbing_command"

echo ""

# SSH security configuration checks
print_section_header "SSH Security Configuration Checks"
ssh_config_check_command="ssh-audit $TARGET"
echo "SSH Security Configuration Checks:"
eval "$ssh_config_check_command"

echo ""

# SSH key fingerprint retrieval
print_section_header "SSH Key Fingerprint Retrieval"
ssh_key_fingerprint_command="ssh-keyscan $TARGET"
echo "SSH Key Fingerprint:"
eval "$ssh_key_fingerprint_command"

echo ""

# SSH authentication methods
print_section_header "SSH Authentication Methods"
ssh_auth_methods_command="ssh -o PreferredAuthentications=none -o PasswordAuthentication=no $TARGET"
echo "SSH Authentication Methods:"
eval "$ssh_auth_methods_command"

echo ""

# SSH user enumeration
print_section_header "SSH User Enumeration"
ssh_user_enum_command="hydra -L users.txt -P passwords.txt $TARGET ssh"
echo "SSH User Enumeration:"
eval "$ssh_user_enum_command"

echo ""

echo "SSH Recon completed."
