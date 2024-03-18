# Flavor Manager

## Repository

- https://github.com/SovereignCloudStack/openstack-flavor-manager

## Relevant references

- https://github.com/SovereignCloudStack/Docs/blob/main/Design-Docs/flavor-naming.md
- https://github.com/osism/openstack-image-manager
- https://github.com/osism/openstack-project-manager

## Requirements

- MUST allow custom flavors

  - MAY auto-generate an SCS name if it can be represented in the SCS spec
  - MUST allow specification of all core flavor properties (such as cpu, ram, ...)

- MUST allow addition of properties (e.g. for scheduling) to custom and SCS-generated flavors
- MUST reject duplicate flavors
- MUST read configuration from a file (e.g. YAML)
- MUST require explicit specification of an ID per flavor (or opt-in to auto-generation of IDs, per flavor)

  - Rationale: IDs cannot be changed once a flavor has been created and it may be very relevant for billing purposes. Once a flavor is defined, it may immediately be used, so it must be correct right from the start.

- MUST handle project-specific flavors (non-public flavors)

  - MUST allow specifying a list of project IDs
  - SHOULD remove project IDs from a flavor which are not listed in the configuration

- SHOULD auto-generate SCS flavors based on hypervisor constraints (max ram, max cpu, ...)
- SHOULD be written in a maintainable language (not bash.)
- SHOULD NOT handle any openstack object except nova flavours

## Open questions

- Should some information be put into flavor metadata instead of or in additional to the name?
- Should this be merged with the openstack-{image,project}-manager into an openstack-manager?
- Should it generate terraform files instead of writing the reconciliation logic on our own? If so, is https://www.terraform.io/cdktf useful?

## Future Work

- volume type manager? (public) network manager?
- cleanup tool (could be imported from OSISM)
