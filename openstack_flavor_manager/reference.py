import logging
import requests
import yaml


def get_url(url: str) -> dict:
    if url == "scs":
        url = "https://raw.githubusercontent.com/SovereignCloudStack/standards/main/Tests/iaas/SCS-Spec.MandatoryFlavors.verbose.yaml"  # noqa: E501
    if url == "osism":
        url = "https://raw.githubusercontent.com/osism/openstack-flavor-manager/main/flavors.yaml"

    logging.debug(f"Loading flavor definitions from {url}")

    result = requests.get(url)
    result.raise_for_status()

    return yaml.safe_load(result.content)
