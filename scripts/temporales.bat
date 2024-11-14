@echo off
del C:\Users\%username%\AppData\Local\Temp /f /s /q
rd C:\Users\%username%\AppData\Local\Temp /s /q
del c:\Windows\Temp /f /s /q
rd c:\Windows\Temp /s /q
exit