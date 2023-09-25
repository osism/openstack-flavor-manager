# Openstack flavor manager

[![PyPi version](https://badgen.net/pypi/v/openstack-flavor-manager/)](https://pypi.org/project/openstack-flavor-manager/)
[![PyPi license](https://badgen.net/pypi/license/openstack-flavor-manager/)](https://pypi.org/project/openstack-flavor-manager/)

Easily create OpenStack flavors based on standardised yaml files

Documentation: <https://docs.scs.community/docs/category/openstack-flavor-manager>


## Usage

```sh
python -m openstack_flavor_manager.main  [OPTIONS]

--name               TEXT  Name of flavor definitions. [default: scs] \
--debug                    Enable debug logging.\
--cloud              TEXT  Cloud name in clouds.yaml. [default: admin]\
--recommended              Create recommended flavors.\
--help                     Show this message and exit.
```

E.g. if you want to create flavors, which belong to the SCS standard, use:

```sh
openstack_flavor_manager --name=scs
```

By default, only the ``mandatory`` flavors are created. If you also want to create the
recommended flavors use ``--recommended`` as in:

```sh
openstack_flavor_manager --recommended --name=scs
```
