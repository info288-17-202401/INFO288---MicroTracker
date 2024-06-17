import json
import sys
import os
# from pydantic import PostgresDsn

def getJsonFile(filename: str):
    try:
        with open(filename, "r") as f:
            json_file = json.load(f)
        print("Using config file {}".format(filename))
        return json_file
    except Exception as e:
        print(e)
        print("Json not found")

# Abrir y cargar el archivo JSON
def getJsonFileFromPath():
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r") as f:
                json_file = json.load(f)
            print("Using config file {}".format(sys.argv[1]))
            return json_file
        except Exception as e:
            print(e)
            print("Json not found")
            sys.exit(1)
    else:
        print("Execute using ./main.py <config_file>")
        sys.exit(1)


def getJsonFilesFromFolder():
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]) :
            folder = sys.argv[1]
            print("Using folder {}".format(folder))
            json_files = []
            for file in os.listdir(folder):
                # Verificar si el file es .json
                if file.endswith('.json'):
                    json_files.append(os.path.join(folder,file))
            return json_files
        else:
            print("Folder not found {folder}".format(folder=sys.argv[1]))
            sys.exit(1)
    else:
        print("Execute using ./main.py <json_folder>")
        sys.exit(1)
