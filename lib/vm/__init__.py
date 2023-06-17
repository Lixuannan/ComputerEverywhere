import json
import logging
import os
import zipfile
from multiprocessing import Process

logging.basicConfig(format="%(levelname)s:\t  %(message)s", level=logging.DEBUG)
_logger = logging.getLogger()


class VM:
    def __init__(
            self,
            new: bool = False,  # False to open an exist VM, True to create a new VM
            name: str = "",  # If you want to create a new vm, this is used to specify the name of the vm
            cpu: int = 2,  # When creating a new vm, you should set the cpu core with this pragma
            ram: float = 4,  # Used to set the ram size when creating a new vm, make sure that the unit is Gigabyte
            template: str = "",  # Initialize the new vm with the template you choose here
            directory: str = ""  # If you are opening an existed vm, use this to specify the directory of it
    ):

        self.name: str = ""
        self.vm_process: Process = Process()
        self.config: dict = {}

        if new:
            if not template:
                _logger.error("No given template of a new VM")
                raise ValueError("No given template of a new VM")

            self.new(name, cpu, ram, template)
        else:
            if not directory:
                _logger.error("No given directory of any VM")
                raise ValueError("No given directory of any VM")

            self.load(directory)

    def load(self, directory: str):
        self.name = directory.split("/")[len(directory.split("/")) - 1]
        _logger.info(f"Loading vm: {self.name}")

        try:
            with open(f"{directory}/config.json", "rt") as f:
                self.config = json.loads(f.read())
        except FileNotFoundError:
            _logger.error("Broken VM")
            raise FileNotFoundError("Broken VM")

    def new(self, name: str, cpu: int, ram: float, template: str):
        _logger.info(f"Creating a new vm with template: {template}")

        template_file = zipfile.ZipFile(template)
        template_file.extractall(f"vms/{name}")

        _logger.info(f"Initializing vm: {name}")
        self.load(f"vms/{name}")
        self.reconfig(cpu=cpu, ram=ram)

    def run(self):
        _logger.info(f"Starting up vm: {self.name}")

        self.vm_process = Process(target=lambda: os.popen(self.config["run_command"].format(cpu, ram)))
        self.vm_process.start()

    def kill(self):
        _logger.warning(f"Killing vm: {name} by sending a SIGKILL signal")
        self.vm_process.kill()

    def reconfig(self, cpu: int = 0, ram: float = 0):
        if cpu:
            self.config["cpu"] = cpu
        if ram:
            self.config["ram"] = ram

        _logger.info(f"Configuring vm: {self.name}")
        with open(f"vms/{self.name}/config.json", "wt") as f:
            f.write(json.dumps(self.config))

    def is_living(self):
        _logger.info(f"Getting vm's stature, current stature is: {self.vm_process.is_alive()}")
        return self.vm_process.is_alive()

    def get_name(self):
        return self.name
