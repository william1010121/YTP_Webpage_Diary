import os
import json
def getJsonData(file_path):
    if not os.path.exists(file_path):
        return {"Data": [], "length": 0}
    with open(file_path) as f:
        data = json.load(f)
    return data
def writeJsonData(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)