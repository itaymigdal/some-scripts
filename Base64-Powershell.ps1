
param(
[Parameter(Mandatory=$true)][string]$string, 
[Parameter(Mandatory=$true)][ValidateSet("encode","decode")]$action
)


function encode ($string)
{
    $EncodedText =[Convert]::ToBase64String([System.Text.Encoding]::unicode.GetBytes($string))
    return $EncodedText
}


function decode ($string)
{
    $DecodedText = [System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($string))
    return $DecodedText
}



Write-Output ""
Write-Output (&$action $string)
Write-Output ""