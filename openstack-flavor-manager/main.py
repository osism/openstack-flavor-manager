import typer
from reference import get_url
from cloud import Cloud
from ensure import Ensure

app = typer.Typer(help="Client to manage OpenStack flavors")


@app.command("ensure")
def ensure(url: str, cloud_backend: str = typer.Option("openstack"), recommended: bool = False) -> None:
    flavour_definitions = get_url(url)  # Get the default values from the reference
    cloud = Cloud(backend=cloud_backend)
    ensure_object = Ensure(cloud=cloud, url=url, recommended=recommended, definitions=flavour_definitions)
    ensure_object.ensure()


def main():
    app()


if __name__ == "__main__":
    main()

