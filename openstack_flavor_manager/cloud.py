# this file contains associations between the name we use in the reference
# files (flavor.yaml) and the respective cloud backend. E.g. the "cpus" item
# relates to "vcpus" in an OpenStack environment.
# Other cloud software might be added in the future.
import logging
from openstack.compute.v2.flavor import Flavor
import openstack
import os


def get_spec_or_default(key_string: str, flavor_spec: dict, defaults: dict):
    if key_string in flavor_spec:
        value = flavor_spec[key_string]
    elif key_string in defaults:
        value = defaults[key_string]
    else:
        raise ValueError(f"Unknown key_string '{key_string}'")

    return value


class Cloud:

    def __init__(self) -> None:
        self.conn = openstack.connect(cloud=os.environ.get("OS_CLOUD"))
        self.existing_flavors = self.conn.list_flavors()
        self.existing_flavor_names = set(flavor.name for flavor in self.existing_flavors)

    def set_flavor(self, flavor_spec: dict, defaults: dict) -> Flavor | None:
        flavor_name = get_spec_or_default(key_string='name', flavor_spec=flavor_spec, defaults=defaults)

        if flavor_name in self.existing_flavor_names:
            logging.warning(f"Flavor with name '{flavor_name}' already exists. Skipping.")
            return None

        flavor = self.conn.create_flavor(
            name=flavor_name,
            ram=get_spec_or_default(key_string='ram', flavor_spec=flavor_spec, defaults=defaults),
            vcpus=get_spec_or_default(key_string='cpus', flavor_spec=flavor_spec, defaults=defaults),
            disk=get_spec_or_default(key_string='disk', flavor_spec=flavor_spec, defaults=defaults),
            ephemeral=0,
            swap=0,
            rxtx_factor=1.0,
            description=get_spec_or_default(key_string='description', flavor_spec=flavor_spec, defaults=defaults),
            is_public=get_spec_or_default(key_string='public', flavor_spec=flavor_spec, defaults=defaults)
        )
        self.conn.set_flavor_specs(
            flavor_id=flavor.id,
            extra_specs={},
        )
        return flavor
