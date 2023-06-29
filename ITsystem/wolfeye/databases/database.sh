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

# MySQL Database Enumeration
print_section_header "MySQL Database Enumeration"
mysql_enum_command="nmap -p 3306 --script mysql-enum $TARGET"
echo "MySQL Database Enumeration:"
eval "$mysql_enum_command"

echo ""

# MS SQL Server Enumeration
print_section_header "MS SQL Server Enumeration"
mssql_enum_command="nmap -p 1433 --script ms-sql-* $TARGET"
echo "MS SQL Server Enumeration:"
eval "$mssql_enum_command"

echo ""

# Oracle Database Enumeration
print_section_header "Oracle Database Enumeration"
oracle_enum_command="nmap -p 1521 --script oracle-sid-brute,oracle-tns-brute $TARGET"
echo "Oracle Database Enumeration:"
eval "$oracle_enum_command"

echo ""

# PostgreSQL Database Enumeration
print_section_header "PostgreSQL Database Enumeration"
postgresql_enum_command="nmap -p 5432 --script postgres-* $TARGET"
echo "PostgreSQL Database Enumeration:"
eval "$postgresql_enum_command"

echo ""

# Elasticsearch Service Enumeration
print_section_header "Elasticsearch Service Enumeration"
elasticsearch_enum_command="nmap -p 9200 --script elasticsearch-* $TARGET"
echo "Elasticsearch Service Enumeration:"
eval "$elasticsearch_enum_command"

echo ""

# MongoDB Database Enumeration
print_section_header "MongoDB Database Enumeration"
mongo_enum_command="nmap -p 27017 --script mongodb-* $TARGET"
echo "MongoDB Database Enumeration:"
eval "$mongo_enum_command"

echo ""

echo "Database Recon completed."
