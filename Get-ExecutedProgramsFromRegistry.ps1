# Script that lists executed programs on a windows machine

function from_registry
    {
    [string []] $list = $null
    # path 1
    $reg_path_1 = "registry::HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store"
    $list += Get-Item -Path $reg_path_1 | Select-Object -ExpandProperty Property
    # path 2
    $reg_path_2 = "registry::HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache"
    $list += Get-Item -Path $reg_path_2 | Select-Object -ExpandProperty Property
    # Remove Duplicates and non-relevant
    $list = $list -like "*.exe*" -notlike "*.ApplicationCompany" -replace ".FriendlyAppName","" | Select-Object -Unique | Sort-Object 
    return $list
    }

from_registry | Out-GridView