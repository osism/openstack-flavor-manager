# SPDX-License-Identifier: Apache-2.0

from typing import List, Dict, Any

from loguru import logger

from .cloud import CloudConnection
from .exceptions import FlavorCreationError
from .models import FlavorSpec, FlavorDefinitions


class FlavorManager:
    """Manages the creation and update of OpenStack flavors."""

    def __init__(
        self,
        cloud_connection: CloudConnection,
        definitions: FlavorDefinitions,
        include_recommended: bool = False,
    ) -> None:
        """Initialize the flavor manager."""
        self.cloud = cloud_connection
        self.definitions = definitions
        self.include_recommended = include_recommended
        self.defaults = definitions.get_defaults()

    def create_flavors(self) -> None:
        """Create all required flavors."""
        flavors_to_create = self._get_flavors_to_create()

        success_count = 0
        error_count = 0

        for flavor_data in flavors_to_create:
            try:
                flavor_spec = FlavorSpec.from_dict(flavor_data, self.defaults)
                self.cloud.create_or_update_flavor(flavor_spec)
                success_count += 1
            except FlavorCreationError as e:
                logger.error(str(e))
                error_count += 1
            except Exception as e:
                logger.error(f"Unexpected error creating flavor: {e}")
                error_count += 1

        logger.info(
            f"Flavor creation completed: {success_count} successful, "
            f"{error_count} failed out of {len(flavors_to_create)} total"
        )

    def _get_flavors_to_create(self) -> List[Dict[str, Any]]:
        """Get the list of flavors to create based on configuration."""
        flavors = self.definitions.mandatory.copy()

        if self.include_recommended:
            flavors.extend(self.definitions.recommended)

        return flavors
