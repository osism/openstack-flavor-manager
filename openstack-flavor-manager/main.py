import typer

from cloud import Cloud
from ensure import Ensure
from validate import Validate

app = typer.Typer(help="Client to manage OpenStack flavors")


@app.command("validate")
def validate(url: str = typer.Argument("scs"), cloudbackend: str = typer.Option("openstack")) -> None:
    cloud = Cloud(backend=cloudbackend)
    object = Validate(cloud=cloud, url=url)
    object.validate()


@app.command("ensure")
def ensure(url: str, cloudbackend: str = typer.Option("openstack"), recommended: bool = False) -> None:
    cloud = Cloud(backend=cloudbackend)
    object = Ensure(cloud=cloud, url=url, recommended=recommended)
    object.ensure()


def main():
    app()


if __name__ == "__main__":
    main()
