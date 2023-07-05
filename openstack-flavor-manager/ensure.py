import logging

from cloud import Cloud
from reference import get_url


logging.basicConfig(format='%(levelname)s: %(message)s')


class Ensure:
    def __init__(self, cloud: Cloud, url: str, recommended: bool = False):
        self.required_flavors = get_url(url, 'mandatory')
        self.cloud = cloud
        if recommended:
            self.required_flavors = self.required_flavors + get_url(url, 'recommended')

    def ensure(self) -> None:
        for required_flavor in self.required_flavors:
            flavor_id = self.cloud.set_flavor(flavor_spec=required_flavor)
            if flavor_id:
                logging.info(f"Flavor created: {required_flavor['name']}")
            else:
                logging.error(f"Flavor could not be created: {required_flavor['name']}")
