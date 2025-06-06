# SPDX-License-Identifier: Apache-2.0

import typer
from typing_extensions import Annotated

from .cloud import CloudConnection
from .config import FlavorSource
from .exceptions import FlavorManagerError
from .logging import configure_logging
from .manager import FlavorManager


app = typer.Typer()


@app.command()
def run(
    name: Annotated[
        str, typer.Option("--name", help="Source of flavor definitions.")
    ] = "scs",
    url: Annotated[
        str, typer.Option("--url", help="Override URL for flavor definitions.")
    ] = None,
    debug: Annotated[
        bool, typer.Option("--debug", help="Enable debug logging.")
    ] = False,
    cloud: Annotated[
        str, typer.Option("--cloud", help="Cloud name in clouds.yaml.")
    ] = "admin",
    recommended: Annotated[
        bool, typer.Option("--recommended", help="Create recommended flavors.")
    ] = False,
) -> None:
    """Create OpenStack flavors based on definitions."""
    configure_logging(debug)

    try:
        # Load flavor definitions
        source = FlavorSource()
        definitions = source.load_definitions(name, url)

        # Connect to cloud
        cloud_connection = CloudConnection(cloud)

        # Create flavors
        manager = FlavorManager(cloud_connection, definitions, recommended)
        manager.create_flavors()

    except FlavorManagerError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(code=1)


def main() -> None:
    """Entry point for the CLI."""
    app()
