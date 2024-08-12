# SPDX-License-Identifier: Apache-2.0

from loguru import logger
from openstack.compute.v2.flavor import Flavor
import openstack
import requests
from requests_file import FileAdapter
import sys
import typer
import typing
import yaml


def get_spec_or_default(key_string: str, flavor_spec: dict, defaults: dict):
    if key_string in flavor_spec:
        value = flavor_spec[key_string]
    elif key_string in defaults:
        value = defaults[key_string]
    # If disc is not present then it is a flavor without disc.
    elif key_string == "disk":
        value = 0
    # By default a flavor should be public
    elif key_string == "public":
        value = True
    # If no flavorid is given, automatically assign one (OpenStack SDK feature)
    elif key_string == "flavorid":
        value = "auto"
    else:
        raise ValueError(f"Unknown key_string '{key_string}'")

    return value


class Cloud:
    def __init__(self, cloud: str) -> None:
        self.conn = openstack.connect(cloud=cloud)
        flavors = self.conn.list_flavors()
        self.existing_flavors = {}
        for flavor in flavors:
            self.existing_flavors[flavor.name] = flavor

    def set_flavor(
        self, flavor_spec: dict, defaults: dict
    ) -> typing.Union[Flavor, None]:
        flavor_name = get_spec_or_default(
            key_string="name", flavor_spec=flavor_spec, defaults=defaults
        )

        if flavor_name not in self.existing_flavors:
            flavor = self.conn.create_flavor(
                name=flavor_name,
                ram=get_spec_or_default(
                    key_string="ram", flavor_spec=flavor_spec, defaults=defaults
                ),
                vcpus=get_spec_or_default(
                    key_string="cpus", flavor_spec=flavor_spec, defaults=defaults
                ),
                disk=get_spec_or_default(
                    key_string="disk", flavor_spec=flavor_spec, defaults=defaults
                ),
                ephemeral=0,
                swap=0,
                rxtx_factor=1.0,
                is_public=get_spec_or_default(
                    key_string="public", flavor_spec=flavor_spec, defaults=defaults
                ),
                flavorid=get_spec_or_default(
                    key_string="flavorid", flavor_spec=flavor_spec, defaults=defaults
                ),
            )
            logger.info(f"Flavor {flavor_name} created")
        else:
            flavor = self.existing_flavors[flavor_name]

        extra_specs = {
            key: value
            for key, value in flavor_spec.items()
            # we could exclude keys explicitly, like so:
            # if key not in ('name', 'ram', 'cpus', 'disk', 'public', 'disabled')
            # but the extra specs should be prefixed, so we can as well do it like so:
            if ":" in key
        }
        self.conn.set_flavor_specs(
            flavor_id=flavor.id,
            extra_specs=extra_specs,
        )
        return flavor


class FlavorManager:
    def __init__(
        self, cloud: Cloud, definitions: dict, recommended: bool = False
    ) -> None:
        self.required_flavors = definitions["mandatory"]
        self.cloud = cloud
        if recommended:
            self.required_flavors = self.required_flavors + definitions["recommended"]

        self.defaults_dict = {}
        for item in definitions["reference"]:
            if "default" in item:
                self.defaults_dict[item["field"]] = item["default"]

    def run(self) -> None:
        for required_flavor in self.required_flavors:
            try:
                self.cloud.set_flavor(
                    flavor_spec=required_flavor, defaults=self.defaults_dict
                )
            except Exception as e:
                logger.error(f"Flavor {required_flavor['name']} could not be created")
                logger.error(e)


def get_flavor_definitions(source: str, url: str) -> dict:
    s = requests.Session()

    if source == "scs":
        source_type = "url"
        url = "https://raw.githubusercontent.com/SovereignCloudStack/standards/main/Tests/iaas/SCS-Spec.MandatoryFlavors.verbose.yaml"  # noqa: E501
    elif source == "osism":
        source_type = "url"
        url = "https://raw.githubusercontent.com/osism/openstack-flavor-manager/main/flavors.yaml"
    elif source == "local":
        source_type = "local"
        if not url:
            url = "file:///data/flavors.yaml"
    elif source == "url":
        source_type = "url"
        if not url:
            raise ValueError(f"No URL specified for source {source}")
    else:
        raise ValueError(f"Unsupported source: {source}")

    if source_type == "local":
        logger.debug(f"Loading flavor definitions from local file {url}")
        s.mount("file://", FileAdapter())
    elif source_type == "url":
        logger.debug(f"Loading flavor definitions from URL {url}")
    else:
        raise ValueError(f"Unsupported source type: {source_type}")

    result = s.get(url)
    result.raise_for_status()

    return yaml.safe_load(result.content)


def run(
    name: str = typer.Option("scs", "--name", help="Source of flavor definitions."),
    url: str = typer.Option(
        None,
        "--url",
        help="Overwrite the default URL where the flavor definitions are available.",
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging."),
    cloud: str = typer.Option("admin", "--cloud", help="Cloud name in clouds.yaml."),
    recommended: bool = typer.Option(
        False, "--recommended", help="Create recommended flavors."
    ),
) -> None:
    if debug:
        level = "DEBUG"
        log_fmt = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
            "<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
    else:
        level = "INFO"
        log_fmt = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
            "<level>{message}</level>"
        )

    logger.remove()
    logger.add(sys.stderr, format=log_fmt, level=level, colorize=True)

    definitions = get_flavor_definitions(name, url)
    manager = FlavorManager(
        cloud=Cloud(cloud), definitions=definitions, recommended=recommended
    )
    manager.run()


def main() -> None:
    typer.run(run)


if __name__ == "__main__":
    main()
