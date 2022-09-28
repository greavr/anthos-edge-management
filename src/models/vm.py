from pydantic import BaseModel

class vm_parameter_set(BaseModel):
    """ Parameter Set """
    name: str
    vm_machine: str
    values: dict

    def __repr__(self):
        return f"""
            name: {self.name},
            vm_machine: {self.vm_machine},
            values: {self.values}"""

class vm_image(BaseModel):
    """" Virtual Machine Info """
    name: str
    image_path: str

    def __repr__(self):
        return f"""
            name: {self.name},
            image_path: {self.image_path}"""

class vm_info(BaseModel):
    """ List of running VMs """
    cluster_name: str
    vm_name: str
    vm_ip: str
    vm_status: str
    vm_image_name: str
    vm_parameter_set_name: str

    def __repr__(self):
        return f"""
        cluster_name: {self.cluster_name},
        vm_name: {self.vm_name},
        vm_ip" {self.vm_ip},
        vm_image_name: {self.vm_image_name},
        vm_parameter_set_name: {self.vm_parameter_set_name},
        vm_status: {self.vm_status}"""