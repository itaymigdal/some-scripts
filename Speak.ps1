
# Define parameters
param(
[Parameter(Mandatory=$false)][string]$string,
[Parameter(Mandatory=$false)][string]$file_path,
[parameter(Mandatory=$false)][int]$volume,
[parameter(Mandatory=$false)][Switch]$woman
)

if ((!$string -and !$file_path) -or ($string -and $file_path))
{
Write-Host "[-] ERROR :: Choose string or a txt file"
exit
}

$speak_object = (new-object -com SAPI.SpVoice)

if ($volume) {$speak_object.volume = $volume}
if ($woman) {$speak_object.voice = $speak_object.GetVoices().item(1)}

if ($file_path)
{$string = Get-Content (Resolve-Path $file_path)}

$speak_object.Speak($string)






