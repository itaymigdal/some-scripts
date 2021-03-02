param
(
    [Parameter (Mandatory=$true)] [string] $input_file, 
    [Parameter (Mandatory=$true)] [string] $output_file,
    [Parameter (Mandatory=$true)] [byte] $byte_key
)

if ((test-path $input_file) -eq $false) 
{
    Write-Host "[-] ERROR: wrong input file" -ForegroundColor Red
    exit
}

if ((test-path $output_file) -eq $true)
{
    Write-Host "[*] WARNING: File" (resolve-path $output_file) "already exists. Override file? [Y]: " -ForegroundColor red -NoNewline
    $answer = Read-Host
    if ($answer -ne "Y") {exit}
}


Set-Content $output_file -Value "" -NoNewline


$input_bytes = Get-Content -Path $input_file -Encoding Byte


try 
{
     foreach ($byte in $input_bytes)
    {
        [byte]$xored_byte = ($byte -bxor $byte_key)
        Add-Content -Value $xored_byte -Path $output_file -Encoding Byte
    }
    Write-host "[+] File" (Resolve-Path $output_file) "created successfully :)"
    
}

catch 
{
    Write-Host "[-] ERROR: Could not write to output file :(" -ForegroundColor Red
    exit
}

