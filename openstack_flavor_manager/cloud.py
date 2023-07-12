# this file contains associations between the name we use in the reference
# files (flavor.yaml) and the respective cloud backend. E.g. the "cpus" item
# relates to "vcpus" in an OpenStack environment.
# Other cloud software might be added in the future.
import openstack
import os


def get_spec_or_default(key_string: str, flavor_spec: dict, defaults: dict) -> object:
    if key_string in flavor_spec:
        return flavor_spec[key_string]
    elif key_string in defaults:
        return defaults[key_string]
    else:
        raise UnknownSpecKeyException


class UnknownSpecKeyException(BaseException):
    pass


class Cloud:

    def __init__(self) -> None:
        self.conn = openstack.connect(cloud=os.environ.get("OS_CLOUD"))

    def get_flavors(self) -> list:
        flavor_list = self.conn.search_flavors()
        return flavor_list

    def set_flavor(self, flavor_spec: dict, defaults: dict) -> int:
        flavor_id = self.conn.create_flavor(
            name=get_spec_or_default(key_string='name', flavor_spec=flavor_spec, defaults=defaults),
            ram=get_spec_or_default(key_string='ram', flavor_spec=flavor_spec, defaults=defaults),
            vcpus=get_spec_or_default(key_string='cpus', flavor_spec=flavor_spec, defaults=defaults),
            disk=get_spec_or_default(key_string='disk', flavor_spec=flavor_spec, defaults=defaults),
            ephemeral=0,
            swap=0,
            rxtx_factor=1.0,
            is_public=get_spec_or_default(key_string='public', flavor_spec=flavor_spec, defaults=defaults)
        )

        self.conn.set_flavor_specs(
            flavor_id=flavor_id,
            extra_specs={},
        )

        return flavor_id
