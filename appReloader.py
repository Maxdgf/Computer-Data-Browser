import sys
import subprocess

def reload():
    call = subprocess.Popen([sys.executable, "app.py"])
    call.communicate()
