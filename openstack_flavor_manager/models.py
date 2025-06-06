# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class FlavorSpec:
    """Represents a flavor specification."""

    name: str
    cpus: int
    ram: int
    disk: int = 0
    public: bool = True
    disabled: bool = False
    flavorid: str = "auto"
    extra_specs: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], defaults: Dict[str, Any]) -> "FlavorSpec":
        """Create FlavorSpec from dictionary with defaults."""
        # Extract basic fields
        basic_fields = {
            "name": data.get("name", defaults.get("name")),
            "cpus": data.get("cpus", defaults.get("cpus")),
            "ram": data.get("ram", defaults.get("ram")),
            "disk": data.get("disk", defaults.get("disk", 0)),
            "public": data.get("public", defaults.get("public", True)),
            "disabled": data.get("disabled", defaults.get("disabled", False)),
            "flavorid": data.get("flavorid", defaults.get("flavorid", "auto")),
        }

        # Extract extra specs (fields with ':' in the key)
        extra_specs = {k: v for k, v in data.items() if ":" in k}

        return cls(**basic_fields, extra_specs=extra_specs)


@dataclass
class ReferenceField:
    """Represents a reference field definition."""

    field: str
    default: Optional[Any] = None
    mandatory_prefix: Optional[str] = None


@dataclass
class FlavorDefinitions:
    """Container for flavor definitions."""

    reference: List[ReferenceField]
    mandatory: List[Dict[str, Any]]
    recommended: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FlavorDefinitions":
        """Create FlavorDefinitions from dictionary."""
        reference = [
            ReferenceField(
                field=ref["field"],
                default=ref.get("default"),
                mandatory_prefix=ref.get("mandatory_prefix"),
            )
            for ref in data.get("reference", [])
        ]

        return cls(
            reference=reference,
            mandatory=data.get("mandatory", []),
            recommended=data.get("recommended", []),
        )

    def get_defaults(self) -> Dict[str, Any]:
        """Extract defaults from reference fields."""
        return {
            ref.field: ref.default for ref in self.reference if ref.default is not None
        }
