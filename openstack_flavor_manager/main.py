import typer
import logging
from openstack_flavor_manager.reference import get_url
from openstack_flavor_manager.cloud import Cloud
from openstack_flavor_manager.ensure import Ensure

app = typer.Typer(help="Client to manage OpenStack flavors")


@app.command("ensure")
def ensure(url: str, cloud_backend: str = typer.Option("openstack"),
           recommended: bool = typer.Option(False, help="Use recommended settings")) -> None:
    flavour_definitions = get_url(url)
    cloud = Cloud()
    ensure_object = Ensure(cloud=cloud, definitions=flavour_definitions, recommended=recommended)
    ensure_object.ensure()


# This is needed for:
# 1) Global app option handling
# 2) Prevent that the single "ensure" command is automatically ommited
@app.callback()
def callback(debug_logging: bool = typer.Option(False, "--debug", help="Enable debug logging")):
    logging.basicConfig(
        level=logging.INFO if not debug_logging else logging.DEBUG,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def main():
    app()


if __name__ == "__main__":
    main()
