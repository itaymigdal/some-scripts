# script for list executed programs on a machine

[string[]]$list=$null
$ErrorActionPreference='silentlycontinue'

# getting registry keys 
$list+=Get-Item -Path "registry::HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store" |
`Select-Object -ExpandProperty Property
$list+=Get-Item -Path "registry::HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Persisted" |
`Select-Object -ExpandProperty Property 
$list+=Get-Item -Path "registry::HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache" |
`Select-Object -ExpandProperty Property
$list+=Get-Item -Path "registry::HKEY_CURRENT_USER\Software\Microsoft\Windows\ShellNoRoam\MUICache" |
`Select-Object -ExpandProperty Property 

# Remove non-relevant & duplicates
$list -like "*.exe*" -notlike '*.ApplicationCompany' -replace '.FriendlyAppName','' | select -Unique | Out-GridView

