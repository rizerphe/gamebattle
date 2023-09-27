import glob
import os

import yaml

all_files = glob.glob("*.yaml")
for file in all_files:
    with open(file) as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)
            print(file)
            exit(1)
        try:
            folder = file[:-5]

            print(f"Validating {folder}")
            print(f"  Name: {data['name']}")
            print(f"  Email: {data['email']}")
            print(f"  Author: {data['author']}")

            if folder != data["email"].split(".")[0]:
                print(f"Folder and email do not match")
                exit(1)
            file = f"{folder}/{data['file']}"
            if not os.path.isfile(file):
                print(f"File {file} does not exist")
                exit(1)
        except KeyError as exc:
            print(f"Key not found: {exc}")
            print(file)
            exit(1)
