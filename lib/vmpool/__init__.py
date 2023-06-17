import json
import logging

from ..vm import VM

logging.basicConfig(format="%(levelname)s:\t  %(message)s", level=logging.DEBUG)
_logger = logging.getLogger()


class VMPool:
    def __init__(self):
        self.pool = []

    def living_vm(self) -> list:
        living_vm = []

        for i in self.pool:
            if i.is_living():
                living_vm.append(i.get_name())

        _logger.info(f"Get living vms successfully, current living vms are: {living_vm}")

        return living_vm

    def all_vm(self) -> list:
        all_vm = []

        for i in self.pool:
            all_vm.append(i.get_name())

        _logger.info(f"Get all vms successfully, current vms are: {all_vm}")

        return all_vm

    def save(self):
        _logger.info("Saving pool to file: vms/vms.json")
        with open("vms/vms.json", "wt") as f:
            f.write(json.dumps(self.pool))

    def submit(self, vm: VM):
        _logger.info(f"Submitting vm: {vm.get_name()}")
        self.add(vm)
        self.run(vm.name)

    def run(self, name: str):
        for i in self.pool:
            if i.get_name() == name:
                i.run()
                break

    def add(self, vm: VM):
        _logger.info(f"Adding vm: {vm.get_name()} to vm pool")
        self.pool.append(vm)
        self.save()

    def clear_pool(self):
        _logger.warning("Cleaning vm pool, killing every vm")

        for i in self.pool:
            i.kill()

    def kill(self, name: str):
        for i in self.pool:
            if i.get_name() == name:
                i.kill()

    def reconfig(self, name: str, cpu: int = 0, ram: float = 0):
        for i in self.pool:
            if i.get_name() == name:
                i.reconfig(cpu=cpu, ram=ram)

