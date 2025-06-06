# SPDX-License-Identifier: Apache-2.0

from typing import Dict, Any

from loguru import logger
import requests
from requests_file import FileAdapter
import yaml

from .exceptions import SourceError, ConfigurationError
from .models import FlavorDefinitions


class FlavorSource:
    """Handles loading flavor definitions from various sources."""

    # Default URLs for known sources
    SOURCES = {
        "scs": (
            "https://raw.githubusercontent.com/SovereignCloudStack/standards/"
            "main/Tests/iaas/SCS-Spec.MandatoryFlavors.verbose.yaml"
        ),
        "osism": "https://raw.githubusercontent.com/osism/openstack-flavor-manager/main/flavors.yaml",
    }

    def __init__(self) -> None:
        """Initialize the flavor source loader."""
        self.session = requests.Session()
        self.session.mount("file://", FileAdapter())

    def load_definitions(self, source: str, url: str = None) -> FlavorDefinitions:
        """Load flavor definitions from the specified source."""
        final_url = self._resolve_url(source, url)
        data = self._fetch_data(final_url)

        try:
            return FlavorDefinitions.from_dict(data)
        except (KeyError, ValueError) as e:
            raise ConfigurationError(f"Invalid flavor definitions format: {e}")

    def _resolve_url(self, source: str, url: str = None) -> str:
        """Resolve the URL based on source type."""
        if source in self.SOURCES:
            logger.debug(f"Using predefined source: {source}")
            return self.SOURCES[source]
        elif source == "local":
            return url or "file:///data/flavors.yaml"
        elif source == "url":
            if not url:
                raise SourceError("URL must be specified when using 'url' source")
            return url
        else:
            raise SourceError(f"Unknown source type: {source}")

    def _fetch_data(self, url: str) -> Dict[str, Any]:
        """Fetch and parse YAML data from URL."""
        try:
            logger.debug(f"Loading flavor definitions from: {url}")
            response = self.session.get(url)
            response.raise_for_status()

            return yaml.safe_load(response.content)

        except requests.RequestException as e:
            raise SourceError(f"Failed to fetch data from {url}: {e}")
        except yaml.YAMLError as e:
            raise SourceError(f"Failed to parse YAML from {url}: {e}")
