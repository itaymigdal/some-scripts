# Finds strings inside files in base path

# Define parameters
param([Parameter(Mandatory=$true)][string]$string, [Parameter(Mandatory=$true)][string]$path)

# For each file
foreach ($file in (Get-ChildItem -Path $path -Recurse -File -Exclude "*.exe","*.dll","*.zip","*.rar","*.7z","*.kdbs","*.ova"))
{

# Checks file name and print if match
if ($file.name -match $string)
{Write-Host "[+]" $file.fullname ": File_Name"}

# For each line checks and print if match
$count = 1
foreach($line in [System.IO.File]::ReadLines($file.fullname))
{
if ($line -match $string)
{Write-Host "[+]" $file.fullname ":" $count}
$count ++
}
}
