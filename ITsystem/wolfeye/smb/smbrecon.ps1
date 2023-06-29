
# Import the necessary modules
Import-Module -Name "CimCmdlets"
Import-Module -Name "SmbShare"

# Set the variable to the target SMB server
$smbServer = "TARGET_SMB_SERVER"

# Retrieve the SMB shares
$shares = Get-SmbShare -CimSession $smbServer

# Display the shares
Write-Output "SMB Shares:"
foreach ($share in $shares) {
    Write-Output "Name: $($share.Name)"
    Write-Output "Path: $($share.Path)"
}

# Retrieve the SMB sessions
$sessions = Get-SmbSession -CimSession $smbServer

# Display the sessions
Write-Output "SMB Sessions:"
foreach ($session in $sessions) {
    Write-Output "User: $($session.ClientUserName)"
    Write-Output "IP Address: $($session.ClientComputerName)"
}

# Retrieve the SMB connections
$connections = Get-SmbConnection -CimSession $smbServer

# Display the connections
Write-Output "SMB Connections:"
foreach ($connection in $connections) {
    Write-Output "Server: $($connection.ServerName)"
    Write-Output "Share: $($connection.ShareName)"
    Write-Output "User: $($connection.UserName)"
}
