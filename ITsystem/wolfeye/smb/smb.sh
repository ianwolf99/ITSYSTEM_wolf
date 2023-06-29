#!/bin/bash

# Check if the IP address argument is provided
if [ $# -lt 1 ]; then
    echo "Please provide an IP address as a command-line argument."
    exit 1
fi

# Define the target IP address
TARGET_IP="$1"

# Function to print section headers
print_section_header() {
    echo "------------------------------------"
    echo "$1"
    echo "------------------------------------"
}

# Nmap scan
print_section_header "Running Nmap scan"
nmap_command="/usr/bin/nmap -p 135,139,445 -T3 -sC --script=smb-enum-* --script-args=unsafe=1 $TARGET_IP"
echo "Nmap Command: $nmap_command"
eval "$nmap_command"

echo ""

# Enum4linux scan
print_section_header "Running Enum4linux scan"
enum4linux_command="/usr/bin/enum4linux -a $TARGET_IP"
echo "Enum4linux Command: $enum4linux_command"
eval "$enum4linux_command"

echo ""

# Nbtscan
print_section_header "Running Nbtscan"
nbtscan_command="/usr/bin/nbtscan $TARGET_IP"
echo "Nbtscan Command: $nbtscan_command"
eval "$nbtscan_command"

echo ""

# Nmblookup
print_section_header "Running Nmblookup"
nmblookup_command="/usr/bin/nmblookup -A $TARGET_IP"
echo "Nmblookup Command: $nmblookup_command"
eval "$nmblookup_command"

echo ""

# CrackMapExec
print_section_header "Running CrackMapExec"
crackmapexec_command="/usr/local/bin/crackmapexec smb $TARGET_IP"
echo "CrackMapExec Command: $crackmapexec_command"
eval "$crackmapexec_command"

echo ""

echo "Scan completed."
