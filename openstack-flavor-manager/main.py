import typer

from cloud import Cloud
from ensure import Ensure

app = typer.Typer(help="Client to manage OpenStack flavors")


@app.command("ensure")
def ensure(url: str, cloudbackend: str = typer.Option("openstack")) -> None:
    cloud = Cloud(backend=cloudbackend)
    object = Ensure(cloud=cloud, url=url)
    object.ensure()


def main():
    app()


if __name__ == "__main__":
    main()
