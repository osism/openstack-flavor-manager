# Openstack flavor manager

Create OpenStack flavors based on a yaml file.

## Usage

```sh
python -m openstack_flavor_manager.main --help
```

E.g. if you want to create flavors, that belong to the SCS standard, use:

```py
python -m openstack_flavor_manager.main ensure scs
```

By default, only the ``mandatory`` flavors are created. If you also want to create the
recommended flavors use ``--recommended`` as in:

```py
python -m openstack_flavor_manager.main ensure --recommended scs
```

If you want to create flavors from your own yaml file, provide a link to this file:

```py
python -m openstack_flavor_manager.main ensure https://my-server.com/my-file.yaml
```

Predefined URL shortcuts are ``scs`` and ``osism``
