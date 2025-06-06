# SPDX-License-Identifier: Apache-2.0


class FlavorManagerError(Exception):
    """Base exception for flavor manager errors."""

    pass


class FlavorCreationError(FlavorManagerError):
    """Exception raised when flavor creation fails."""

    pass


class ConfigurationError(FlavorManagerError):
    """Exception raised for configuration related errors."""

    pass


class SourceError(FlavorManagerError):
    """Exception raised when flavor source cannot be loaded."""

    pass
