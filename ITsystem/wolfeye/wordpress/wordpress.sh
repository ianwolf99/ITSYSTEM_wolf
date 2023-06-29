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
nmap_http_command="nmap -p 80,443 --script http-enum,http-vuln*,http-wordpress*,http-shellshock $TARGET"
echo "Nmap Command:"
echo "$nmap_http_command"
eval "$nmap_http_command"

echo ""

# WordPress version detection
print_section_header "WordPress Version Detection"
wordpress_version_command="wpscan --url $TARGET --enumerate v"
echo "WordPress Version Detection:"
eval "$wordpress_version_command"

echo ""

# WordPress theme and plugin enumeration
print_section_header "WordPress Theme and Plugin Enumeration"
wordpress_enumeration_command="wpscan --url $TARGET --enumerate t,p"
echo "WordPress Theme and Plugin Enumeration:"
eval "$wordpress_enumeration_command"

echo ""

# WordPress username enumeration
print_section_header "WordPress Username Enumeration"
wordpress_username_enum_command="wpscan --url $TARGET --enumerate u"
echo "WordPress Username Enumeration:"
eval "$wordpress_username_enum_command"

echo ""

# WordPress vulnerability scanning
print_section_header "WordPress Vulnerability Scanning"
wordpress_vulnerability_scan_command="wpscan --url $TARGET --enumerate vp"
echo "WordPress Vulnerability Scanning:"
eval "$wordpress_vulnerability_scan_command"

echo ""

# WordPress configuration file disclosure
print_section_header "WordPress Configuration File Disclosure"
wordpress_config_disclosure_command="wpscan --url $TARGET --enumerate c"
echo "WordPress Configuration File Disclosure:"
eval "$wordpress_config_disclosure_command"

echo ""

# WordPress timthumb vulnerability scanning
print_section_header "WordPress TimThumb Vulnerability Scanning"
timthumb_scan_command="wpscan --url $TARGET --enumerate tt"
echo "WordPress TimThumb Vulnerability Scanning:"
eval "$timthumb_scan_command"

echo ""

# WordPress users enumeration
print_section_header "WordPress Users Enumeration"
wordpress_users_enum_command="wpscan --url $TARGET --enumerate u"
echo "WordPress Users Enumeration:"
eval "$wordpress_users_enum_command"

echo ""

echo "WordPress Recon completed."
