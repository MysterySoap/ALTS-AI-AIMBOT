import os
import urllib.request
import zipfile
import json
import shutil
import subprocess

try:
    newest_version = "https://raw.githubusercontent.com/MysterySoap/ALTS-AI-AIMBOT/main/current_version.txt"
    req = urllib.request.Request(newest_version, headers={'Cache-Control': 'no-cache'})
    response = urllib.request.urlopen(req)
    remote_version = response.read().decode().strip()

    file_paths = [
        "./ALTS.py",
        "./yolo.cfg",
        "./yolo.weights",
        "./req.txt",
        "./current_version.txt",
    ]

    localv_path = "localv.json"

    if not os.path.exists(localv_path) or not os.path.exists(file_paths[1]):
        local_version = "0.0.0"
        data = {
            "version": remote_version,
            "pip": False
        }
        with open(localv_path, "w") as file:
            json.dump(data, file)
    else:
        with open(localv_path, "r") as file:
            data = json.load(file)
            local_version = data["version"]

    if remote_version != local_version:
        option = True if input("Your version of ALTS is out of date, would you like to update? (y/n): ").lower() == "y" else False
        if option:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Error occurred while removing {file_path}: {e}")

            print("Downloading...")
            # Download the zip file
            url = "https://github.com/MysterySoap/ALTS-AI-AIMBOT/archive/refs/tags/ai2.zip"
            response = urllib.request.urlopen(url)
            zip_content = response.read()

            # Save the zip file
            with open("ai-aimbot.zip", "wb") as file:
                file.write(zip_content)

            print("Unzipping...")
            # Unzip the file
            with zipfile.ZipFile("ai-aimbot.zip", "r") as zip_ref:
                zip_ref.extractall("ai-aimbot")
            os.remove("ai-aimbot.zip")

            print("Moving files...")
            # Move files from ai-aimbot/ to current directory
            for root, dirs, files in os.walk("ai-aimbot"):
                for file in files:
                    shutil.move(os.path.join(root, file), os.path.join(".", file))

            # Remove ai-aimbot-testing/ directory
            shutil.rmtree("ai-aimbot")

            with open("localv.json", "w") as file:
                data["version"] = remote_version
                json.dump(data, file)

            with open("localv.json", "r") as file:
                data2 = json.load(file)
                pip = data["pip"]

            if pip is not True:
                print("Installing required modules...")
                os.system("pip install -r req.txt")
                os.system("pip3 install -r req.txt")
                with open("localv.json", "w") as file:
                    data2["pip"] = True
                    json.dump(data2, file)

    subprocess.run(["python", "ALTS.py"])

except KeyboardInterrupt:
    exit()
