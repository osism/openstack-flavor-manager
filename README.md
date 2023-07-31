# Openstack flavor manager

[![PyPi version](https://badgen.net/pypi/v/openstack-flavor-manager/)](https://pypi.org/project/openstack-flavor-manager/)
[![PyPi license](https://badgen.net/pypi/license/openstack-flavor-manager/)](https://pypi.org/project/openstack-flavor-manager/)

Easily create OpenStack flavors based on standardised yaml files

Documentation: <https://docs.scs.community/docs/category/openstack-flavor-manager>


## Usage

```sh
python -m openstack_flavor_manager.main --help
```

E.g. if you want to create flavors, which belong to the SCS standard, use:

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
