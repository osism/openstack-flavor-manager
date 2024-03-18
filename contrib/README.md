# contrib folder

## requirements.md

This document contains the requirements for a potential flavor-manager
tool as discussed in an SCS-related team meeting on Apr 21, 2022,
prior to the conception of this tool. It is merely kept for the record.

## flavor_generator.py

This tool creates possible SCS flavors by a given _rules.yaml_ file.
With the provided example file it creates 145206019 flavors.
The runtime is about 45 seconds.
If you pipe them to a file, it will be about 4.4G large.

## Usage

```sh
python3 flavor_generator.py
```

Feel free to change values inside the _rules.yaml_ file.
