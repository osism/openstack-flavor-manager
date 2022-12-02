# this file contains associations between the name we use in the reference
# files (flavor.yaml) and the respective cloud backend. E.g. the "cpus" item
# relates to "vcpus" in an OpenStack environment.
# Other cloud software might be added in the future.
import openstack
import os


class Cloud:
    openstack = {
        "name": "name",
        "cpus": "vcpus",
        "ram": "ram",
        "disk": "disk",
        "public": "os-flavor-access:is_public",
        "disabled": "is_disabled",
    }

    def __init__(self, backend: str) -> None:
        self.backend = backend
        self.conn = openstack.connect(cloud=os.environ.get("OS_CLOUD"))

    def get_reference(self, key: str) -> dict:
        if self.backend == "openstack":
            return self.openstack[key]

    def get_flavors(self) -> list:
        if self.backend == "openstack":
            flavor_list = self.conn.search_flavors()
            return flavor_list

    def set_flavor(self, flavor_spec: dict) -> int:
        if self.backend == "openstacks":
            flavor_id = self.conn.create_flavor(
                name=flavor_spec['name'],
                ram=flavor_spec['ram'],
                vcpus=flavor_spec['cpus'],
                disk=flavor_spec['disk'],
                ephemeral=0,
                swap=0,
                rxtx_factor=1.0,
                is_public=flavor_spec['public']
            )
            # description
            # properties
            # extra-specs
            self.cloud.conn.set_flavor_specs(
                flavor_id=flavor_id,
                extra_specs=...,
            )
            return flavor_id
