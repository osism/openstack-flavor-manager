import requests
import yaml


def get_url(url: str) -> dict:
    if url == "scs":
        url = "https://raw.githubusercontent.com/SovereignCloudStack/standards/main/Tests/iaas/SCS-Spec.MandatoryFlavors.verbose.yaml"
    if url == "osism":
        url = "https://raw.githubusercontent.com/osism/openstack-flavor-manager/main/flavors.yaml"

    result = requests.get(url)
    try:
        result = yaml.safe_load(result.content)
        return result
    except yaml.YAMLError as exc:
        print(exc)
