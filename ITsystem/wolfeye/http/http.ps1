
Install-Module -Name Nmap

# Next, import the modules for http and nmap

Import-Module -Name Microsoft.PowerShell.Utility
Import-Module -Name Nmap

# Now, perform an http request to gather information

$uri = "http://www.example.com"
$result = Invoke-WebRequest -Uri $uri

# Display the headers and content of the http response

Write-Host "HTTP Headers:"
$result.Headers
Write-Host "HTTP Content:"
$result.Content

# Finally, use nmap to perform a port scan

$nmap = $env:ProgramFiles + "\Nmap\\nmap.exe"
$portScan = $nmap + " -p 1-1000 -oN portscan.txt " + $uri

Write-Host "Running nmap port scan..."
Invoke-Expression -Command $portScan

# Display the results of the nmap port scan

Write-Host "Nmap Port Scan Results:"
Get-Content -Path "portscan.txt"