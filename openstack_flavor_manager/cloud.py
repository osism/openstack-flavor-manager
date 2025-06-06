# SPDX-License-Identifier: Apache-2.0

from typing import Dict, Optional

from loguru import logger
from openstack.compute.v2.flavor import Flavor
import openstack

from .exceptions import FlavorCreationError
from .models import FlavorSpec


class CloudConnection:
    """Manages OpenStack cloud connection and flavor operations."""

    def __init__(self, cloud: str) -> None:
        """Initialize cloud connection and load existing flavors."""
        try:
            self.conn = openstack.connect(cloud=cloud)
        except Exception as e:
            raise FlavorCreationError(f"Failed to connect to cloud '{cloud}': {e}")

        self.existing_flavors: Dict[str, Flavor] = {}
        self._load_existing_flavors()

    def _load_existing_flavors(self) -> None:
        """Load all existing flavors from the cloud."""
        try:
            flavors = self.conn.list_flavors()
            for flavor in flavors:
                self.existing_flavors[flavor.name] = flavor
        except Exception as e:
            logger.warning(f"Failed to load existing flavors: {e}")

    def create_or_update_flavor(self, flavor_spec: FlavorSpec) -> Optional[Flavor]:
        """Create a new flavor or update existing one."""
        try:
            if flavor_spec.name not in self.existing_flavors:
                flavor = self._create_flavor(flavor_spec)
                logger.info(f"Flavor {flavor_spec.name} created")
            else:
                flavor = self.existing_flavors[flavor_spec.name]
                logger.debug(f"Flavor {flavor_spec.name} already exists")

            # Update extra specs
            if flavor_spec.extra_specs:
                self._update_extra_specs(flavor, flavor_spec.extra_specs)

            return flavor

        except Exception as e:
            raise FlavorCreationError(
                f"Failed to create/update flavor '{flavor_spec.name}': {e}"
            )

    def _create_flavor(self, flavor_spec: FlavorSpec) -> Flavor:
        """Create a new flavor in OpenStack."""
        return self.conn.create_flavor(
            name=flavor_spec.name,
            ram=flavor_spec.ram,
            vcpus=flavor_spec.cpus,
            disk=flavor_spec.disk,
            ephemeral=0,
            swap=0,
            rxtx_factor=1.0,
            is_public=flavor_spec.public,
            flavorid=flavor_spec.flavorid,
        )

    def _update_extra_specs(self, flavor: Flavor, extra_specs: Dict[str, str]) -> None:
        """Update flavor extra specs."""
        try:
            self.conn.set_flavor_specs(
                flavor_id=flavor.id,
                extra_specs=extra_specs,
            )
            logger.debug(f"Updated extra specs for flavor {flavor.name}")
        except Exception as e:
            logger.warning(
                f"Failed to update extra specs for flavor {flavor.name}: {e}"
            )
