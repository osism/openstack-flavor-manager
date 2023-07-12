import logging
from cloud import Cloud


class Ensure:
    def __init__(self, cloud: Cloud, url: str, definitions: dict, recommended: bool = False) -> None:
        self.required_flavors = definitions['mandatory']
        self.cloud = cloud
        if recommended:
            self.required_flavors = self.required_flavors + definitions['recommended']

        self.defaults_dict = {}
        for item in definitions['reference']:
            if 'default' in item:
                self.defaults_dict[item['field']] = item['default']

    def ensure(self) -> None:
        for required_flavor in self.required_flavors:
            flavor_id = self.cloud.set_flavor(flavor_spec=required_flavor, defaults=self.defaults_dict)
            if flavor_id:
                logging.info(f"Flavor created: {required_flavor['name']}")
            else:
                logging.error(f"Flavor could not be created: {required_flavor['name']}")
