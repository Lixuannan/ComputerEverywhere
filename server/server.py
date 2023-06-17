import json
import logging.config

import uvicorn
from fastapi import *

import lib.vm
import lib.vmpool

app = FastAPI()

logging.basicConfig(format="%(levelname)s:\t  %(message)s", level=logging.DEBUG)
logger = logging.getLogger()

pool = lib.VMPool()


@app.get("/")
def get_root() -> str:
    return "Welcome to ComputerEverywhere 's api server"


@app.get("/all_vm")
def all_vm(api_key: str = ""):
    if not api_key == config["api_key"]:
        logger.error("Wrong api_key, please check and try again later")
        return {"error": "Wrong api_key, please check and try again later"}

    try:
        all_vms = pool.all_vm()
    except:
        return {"error": "UnKnown error, please try again later"}

    return all_vms


@app.get("/living_vm")
def living_vm(api_key: str = ""):
    if not api_key == config["api_key"]:
        logger.error("Wrong api_key, please check and try again later")
        return {"error": "Wrong api_key, please check and try again later"}

    try:
        living_vms = pool.living_vm()
    except:
        return {"error": "UnKnown error, please try again later"}

    return living_vms


@app.get("/new_vm")
def new_vm(name: str, cpu: int, ram: float, template: str, api_key: str = ""):
    if not api_key == config["api_key"]:
        logger.error("Wrong api_key, please check and try again later")
        return {"error": "Wrong api_key, please check and try again later"}

    vm = lib.VM(
        new=True,
        name=name,
        cpu=cpu,
        ram=ram,
        template=template
    )

    pool.add(vm)


@app.get("/reconfig")
def reconfig(name: str, cpu: int = 0, ram: float = 0, api_key: str = ""):
    if not api_key == config["api_key"]:
        logger.error("Wrong api_key, please check and try again later")
        return {"error": "Wrong api_key, please check and try again later"}

    pool.reconfig(name=name, cpu=cpu, ram=ram)


@app.get("/run")
def run(name: str, api_key: str = ""):
    if not api_key == config["api_key"]:
        logger.error("Wrong api_key, please check and try again later")
        return {"error": "Wrong api_key, please check and try again later"}

    try:
        port = pool.run(name=name)
        return {"port": port}
    except IOError:
        return {"error": f"No empty port exist, cannot start vm: {name}"}


if __name__ == '__main__':
    with open("config.json", "rt") as f:
        config = json.loads(f.read())

    logger.info(
        f"Config loaded successfully.\n\t\t\t host: {config['host']} \t "
        f"port: {config['port']} \t api_key: {config['api_key']}")

    uvicorn.run(
        app=app,
        host=config["host"],
        port=config["port"]
    )
