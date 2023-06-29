# Check if the IP address argument is provided
if ($args.Length -lt 1) {
    Write-Host "Please provide an IP address as a command-line argument."
    exit
}

$IPAddress = $args[0]
$outputFile = "C:\Users\Sana\Desktop\ITSystem\ITsystem\wolfeye\smb_results.txt"

$nmapCommand = "C:\Users\Sana\Desktop\ITSystem\ITsystem\wolfeye\Nmap\nmap.exe -p 135,139,445 -T 3 -sV -A -sC $IPAddress -oN $outputFile -Pn   "
Invoke-Expression -Command $nmapCommand



#$scanResults = Get-Content -Path $outputFile -Raw


#$scanResults

#$additionalScanResults = Get-Content -Path "smb_additional_scan_results.txt"
#$additionalScanResults

