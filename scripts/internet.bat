@echo off
ipconfig /release
ipconfig /renew
ipconfig /flushdns
netsh winsock reset
netsh advfirewall firewall add rule name="StopThrottling" dir=in action=block remoteip=173.194.55.0/24,206.111.0.0/16 enable=yes