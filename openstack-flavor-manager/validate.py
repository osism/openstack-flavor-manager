import logging

from cloud import Cloud
from reference import get_url
from scs_naming_validator import scs_naming_is_valid


logging.basicConfig(format='%(levelname)s: %(message)s')


class Validate:
    def __init__(self, cloud: Cloud, url: str):
        self.required_reference = get_url(url, 'reference')
        self.required_flavors = get_url(url, 'mandatory')
        self.current_flavors = cloud.get_flavors()
        self.cloud = cloud

    def check_for_mandatory_standards(self) -> None:
        # loop through all reference flavors
        for required_flavor in self.required_flavors:
            matched_flavor = {}

            # loop through all falvors on the targeted cloud
            for current_flavor in self.current_flavors:
                # find matching flavors
                if current_flavor[self.cloud.get_reference(key="name")] == required_flavor['name']:
                    matched_flavor = current_flavor
                    break
            else:
                # if no match was found, generate an error entry
                logging.error(f"Flavor is missing: {required_flavor['name']}")
                # continue, to skip detailed field validation
                continue

            # loop through all required flavor-fields of the reference
            for reference in self.required_reference:

                # check if the reference has a default value
                if "default" in reference:
                    reference_value = reference['default']
                # otherwise use the required_flavor value
                else:
                    reference_value = required_flavor[reference['field']]

                # check if the fields value is equal to the reference value
                if reference_value != matched_flavor[self.cloud.get_reference(key=reference['field'])]:
                    msg = f"Mismatch in flavor {required_flavor['name']} field {reference['field']}. "
                    msg = msg + f"Value is: {matched_flavor[self.cloud.get_reference(key=reference['field'])]}. "
                    msg = msg + f"Value should: {required_flavor[reference['field']]}"
                    logging.error(msg)

    def check_for_optional_standards(self) -> None:
        # find prefixes for flavor namings
        for item in self.required_reference:
            if item['field'] == "name":
                mandatory_prefix = item['mandatory_prefix']
                optional_prefix = item['optional_prefix']
                break

        # reverse lookup to find flavors by prefix that are not in the reference
        for current_flavor in self.current_flavors:
            current_flavor_name = current_flavor[self.cloud.get_reference(key="name")]

            # If flavor does not start with one of the prefixes, skip the flavor
            if not current_flavor_name.startswith(mandatory_prefix):
                continue
            if not current_flavor_name.startswith(optional_prefix):
                continue

            # loop through all reference flavors
            for required_flavor in self.required_flavors:
                # find matching flavors
                if required_flavor['name'] == current_flavor_name:
                    break
            else:
                # if no match was found in the reference found, generate an error
                # entry if the flavor name starts with the mandatory_prefix
                if current_flavor_name.startswith(mandatory_prefix):
                    logging.error(f"Flavor should not exist: {current_flavor_name}")
                # validate the naming pattern / grammar of the flavor
                else:
                    if self.url == "scs":
                        if not scs_naming_is_valid(current_flavor):
                            logging.error(f"Flavor name is invalid: {current_flavor_name}")

    def validate(self) -> None:
        self.check_for_mandatory_standards()
        self.check_for_optional_standards()
