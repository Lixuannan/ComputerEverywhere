from fastapi import *

import json

app = FastAPI()


@app.get("/")
def get_root() -> str:
    return "Welcome to ComputerEverywhere 's api server"


@app.get("/ls_vm")
def ls_vm():
    try:
        with open("server/vms/vms.json", "rt") as f:
            vms_json = json.loads(f.read())
        return vms_json["vms"]
    except FileNotFoundError:
        return "VMs config file not found, please check the file and try again"
    except json.JSONDecodeError:
        return "Broken JSON config file, please check the json config file"
    except KeyError:
        return "Broken JSON config file, please check the json config file"
