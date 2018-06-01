
import subprocess
import psutil
import time
name =[]

while True:
    for proc in psutil.process_iter():
        name.append(proc.name())
    try:
        name.index("python3.5")
        type(i)
        time.sleep(300)
    except:
        subprocess.Popen("sh scr.sh", shell=True)
        i=0
