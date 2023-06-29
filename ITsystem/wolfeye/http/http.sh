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

# Nmap scan for open HTTP ports and version detection
print_section_header "Nmap Scan - Open HTTP Ports and Version Detection"
nmap_command="nmap -p 80,443,8080,8000,8888,8008,8181,8081,8880,8889 -sC -v -A --script=http* $TARGET"
echo "Nmap Command:"
echo "$nmap_command"
eval "$nmap_command"

echo ""

# Nmap scan with NSE scripts for additional HTTP reconnaissance
#print_section_header "Nmap Scan - Additional HTTP Reconnaissance"
#nmap_http_recon_command="nmap -p 80,443 --script=http-enum,http-vuln* $TARGET"
#echo "Nmap Command:"
#echo "$nmap_http_recon_command"
#eval "$nmap_http_recon_command"

echo ""

# HTTP version detection
print_section_header "HTTP Version Detection"
http_version_command="curl -sI $TARGET | grep 'HTTP'"
echo "HTTP Version:"
eval "$http_version_command"

echo ""

# Banner grabbing
print_section_header "Banner Grabbing"
banner_grabbing_command="curl -sI $TARGET"
echo "Banner:"
eval "$banner_grabbing_command"

echo ""

# Web technology identification
print_section_header "Web Technology Identification"
wappalyzer_command="wappalyzer -u $TARGET"
echo "Web Technologies:"
eval "$wappalyzer_command"

echo ""

# WHOIS lookup
print_section_header "WHOIS Lookup"
whois_lookup_command="whois $TARGET"
echo "WHOIS Lookup:"
eval "$whois_lookup_command"

echo ""

# Security misconfiguration checks
print_section_header "Security Misconfiguration Checks"
nikto_command="nikto -h $TARGET -T x"
echo "Security Misconfiguration Checks:"
eval "$nikto_command"

echo ""

# SSL/TLS certificate information
print_section_header "SSL/TLS Certificate Information"
ssl_info_command="openssl s_client -connect $TARGET:443 2>/dev/null | openssl x509 -noout -text"
echo "SSL/TLS Certificate Information:"
eval "$ssl_info_command"

echo ""

# DNS information
print_section_header "DNS Information"
dns_info_command="nslookup $TARGET"
echo "DNS Information:"
eval "$dns_info_command"

echo ""

echo "Recon completed."
