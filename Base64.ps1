
param(
[Parameter(Mandatory=$true)][string]$string, 
[Parameter(Mandatory=$true)][ValidateSet("encode","decode")]$action,
[Parameter(Mandatory=$false)][int]$iterations=1
)


function encode ($string)
{
    $EncodedText =[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($string))
    return $EncodedText
}


function decode ($string)
{
    $DecodedText = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($string))
    return $DecodedText
}


$results = @()
$results += $string

for ($i = 0; $i -le ($iterations - 1); $i ++)
{
    $results += (&$action $results[$i])
}

Write-Output ""
Write-Output $results[$iterations]
Write-Output ""