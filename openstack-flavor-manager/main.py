import typer

from cloud import Cloud
from ensure import Ensure

app = typer.Typer(help="Client to manage OpenStack flavors")


@app.command("ensure")
def ensure(url: str, cloudbackend: str = typer.Option("openstack"), recommended: bool = False) -> None:
    cloud = Cloud(backend=cloudbackend)
    object = Ensure(cloud=cloud, url=url, recommended=recommended)
    object.ensure()

# Add empty callback to enable "ensure" as a single command in typer
@app.callback()
def callback():
    pass

def main():
    app()


if __name__ == "__main__":
    main()
