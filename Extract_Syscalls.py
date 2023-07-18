import pefile

ntdll_path = r"C:\windows\system32\ntdll.dll"

exports = {}

# Parse zw exports
ntdll = pefile.PE(ntdll_path)
for e in ntdll.DIRECTORY_ENTRY_EXPORT.symbols:
    try:
        export_name = e.name.decode()
        if export_name.startswith("Zw"):
            exports[e.address] = export_name
    except AttributeError as e:
        pass
exports = dict(sorted(exports.items()))

i = 0x00
for export in exports:
    print(exports[export], hex(i))
    i += 1
