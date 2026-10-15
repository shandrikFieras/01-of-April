#reg.exe add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize /v AppsUseLightTheme /t REG_DWORD /d 0 /f
#Светлая Тема:

#reg.exe add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize /v AppsUseLightTheme /t REG_DWORD /d 1 /f
#Переключиться на темный режим в Python можно с помощью пакета subprocess следующим образом:

import subprocess
import random
command = ['reg.exe', 'add', 'HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize',
           '/v', 'AppsUseLightTheme', '/t', 'REG_DWORD', '/d', random.choice(['0', '1']), '/f']
subprocess.Popen(command)
