import typer
import logging
from reference import get_url
from cloud import Cloud
from ensure import Ensure

app = typer.Typer(help="Client to manage OpenStack flavors")


@app.command("ensure")
def ensure(url: str, cloud_backend: str = typer.Option("openstack"), recommended: bool = False) -> None:
    flavour_definitions = get_url(url)
    cloud = Cloud()
    ensure_object = Ensure(cloud=cloud, url=url, definitions=flavour_definitions, recommended=recommended)
    ensure_object.ensure()


# Add empty callback to enable "ensure" as a single command in typer
@app.callback()
def callback():
    pass


def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    app()


if __name__ == "__main__":
    main()
