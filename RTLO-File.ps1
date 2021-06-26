param
(
   [Parameter(Mandatory=$true)][string] $real_extension,
   [Parameter(Mandatory=$true)][string] $fake_extension,
   [Parameter(Mandatory=$true)][string] $file_path
)

$rtlo_encoding = [char]0x202e
$file_name_place_Holder = "REPLACE"
$fake_extension_reverse = -join[regex]::Matches($fake_extension,".",'RightToLeft')

$new_filename = (Split-Path (resolve-path $file_path)) + "\" + $file_name_place_Holder + $rtlo_encoding + $fake_extension_reverse + "." + $real_extension

Rename-Item -Path $file_path -NewName $new_filename 

