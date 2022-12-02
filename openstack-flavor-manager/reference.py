import requests
import yaml


def get_url(url: str, key: str) -> list:
    if url == "scs":
        url = "https://raw.githubusercontent.com/SovereignCloudStack/standards/main/flavors.yaml"
    if url == "osism":
        url = "https://raw.githubusercontent.com/osism/openstack-flavor-manager/main/flavors.yaml"

    result = requests.get(url)
    try:
        result = yaml.safe_load(result.content)
    except yaml.YAMLError as exc:
        print(exc)

    return result[key]
