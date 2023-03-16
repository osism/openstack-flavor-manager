import requests
import yaml


def get_url(url: str, key: str) -> list:
    if url == "scs":
        url = "https://raw.githubusercontent.com/SovereignCloudStack/standards/main/Tests/iaas/SCS-Spec.MandatoryFlavors.verbose.yaml"
    if url == "osism":
        url = "https://raw.githubusercontent.com/osism/openstack-flavor-manager/main/flavors.yaml"

    result = requests.get(url)
    try:
        result = yaml.safe_load(result.content)
    except yaml.YAMLError as exc:
        print(exc)

    # depending on the source of origin, the data might need to be cleaned up
    cleaned_list = []
    for item in result[key]:
        # scs exports a field description which has to be ignored
        if "description" in item:
            item.pop("description")
        cleaned_list.append(item)

    result[key] = cleaned_list

    return result[key]
