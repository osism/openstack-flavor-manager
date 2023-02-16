# Openstack flavor manager

Create OpenStack flavors based on a yaml file.

## Usage

```sh
python3 main.py --help
```

E.g. if you want to create flavors, that belong to the SCS standard, use:

```py
python3 main.py ensure scs
```

If you want to create flavors from your own yaml file, provide a link to this file:

```py
python3 main.py ensure https://my-server.com/my-file.yaml
```
