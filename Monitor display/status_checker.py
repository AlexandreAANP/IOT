import subprocess
import time

script_name = "Screen_Show.py" # Replace with the name of your script 
script_path = "./screen_display/Screen_Show.py" # Replace with the path to your script 

while True:
    process = subprocess.Popen(["python3", script_path])

    time.sleep(100)

    process.terminate()
    process.wait()
