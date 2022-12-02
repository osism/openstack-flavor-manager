# generate possible scs flavors
import itertools
import yaml

with open("./rules.yaml", "r") as stream:
    try:
        rules = yaml.safe_load(stream=stream)
    except yaml.YAMLError as exc:
        print(exc)

# prefixes
prefixes = rules['prefixes']
# cpus
cpus = []
cpu_counts = rules['cpu_counts']
cpu_suffixes = rules['cpu_suffixes']
cpu_securities = rules['cpu_securities']
# rams
rams = []
ram_counts = rules['ram_counts']
ram_suffixes = rules['ram_suffixes']
# disks (optional)
disks = [""]  # allow empty
disk_suffixes = rules['disk_suffixes']
disk_amounts = rules['disk_amounts']
disk_sizes = rules['disk_sizes']
# virtualizations (optional)
virtualizations = [""]  # allow empty
hypervisors = rules['hypervisors']
nesteds = rules['nesteds']
# archs (optional)
archs = [""]  # allow empty
arch_vendors = rules['arch_vendors']
arch_generations = rules['arch_generations']
arch_frequencies = rules['arch_frequencies']
# gpus (optional)
gpus = [""]  # allow empty
gpu_modes = rules['gpu_modes']
gpu_models = rules['gpu_models']
gpu_hbms = rules['gpu_hbms']

# special (optional) - all combinations possible
sepcials = [""]  # allow empty
special_list = rules['specials']


#########################################
# build cpus array
#########################################
for cpu_count in cpu_counts:
    for cpu_suffix in cpu_suffixes:
        cpus.append(f"{cpu_count}{cpu_suffix}")
for cpu_count in cpu_counts:
    for cpu_suffix in cpu_suffixes:
        for cpu_security in cpu_securities:
            cpus.append(f"{cpu_count}{cpu_suffix}{cpu_security}")


#########################################
# build rams array
#########################################
for ram_count in ram_counts:
    rams.append(f"{ram_count}")
for ram_count in ram_counts:
    for ram_suffix in ram_suffixes:
        rams.append(f"{ram_count}{ram_suffix}")


#########################################
# build disks array
#########################################
# add only disk suffixes
for disk_suffix in disk_suffixes:
    disks.append(f":{disk_suffix}")
# add only disk sizes
for disk_size in disk_sizes:
    disks.append(f":{disk_size}")
# add only disk sizes with suffix
for disk_size in disk_sizes:
    for disk_suffix in disk_suffixes:
        disks.append(f":{disk_size}{disk_suffix}")
# add only disk amounts
for disk_amount in disk_amounts:
    disks.append(f":{disk_amount}")
# add only disk amounts with suffixes
for disk_amount in disk_amounts:
    for disk_suffix in disk_suffixes:
        disks.append(f":{disk_amount}{disk_suffix}")
# add disk sizes with disk amounts
for disk_amount in disk_amounts:
    for disk_size in disk_sizes:
        disks.append(f":{disk_amount}{disk_size}")
# add disk sizes with disk amounts and suffixes
for disk_amount in disk_amounts:
    for disk_size in disk_sizes:
        for disk_suffix in disk_suffixes:
            disks.append(f":{disk_amount}{disk_size}{disk_suffix}")


#########################################
# build virtualizations
#########################################
# add only hypervisors
for hypervisor in hypervisors:
    virtualizations.append(f"-{hypervisor}")
# add only nesteds
for nested in nesteds:
    virtualizations.append(f"-{nested}")
# add hypervisors with nesteds
for hypervisor in hypervisors:
    for nested in nesteds:
        virtualizations.append(f"-{hypervisor}-{nested}")


#########################################
# build archs
#########################################
# add only arch vendors
for arch_vendor in arch_vendors:
    archs.append(f"-{arch_vendor}")
# add arch vendor with generation
for arch_vendor in arch_vendors:
    for arch_generation in arch_generations:
        archs.append(f"-{arch_vendor}{arch_generation}")
# add arch vendor with hbm
for arch_vendor in arch_vendors:
    for arch_frequency in arch_frequencies:
        archs.append(f"-{arch_vendor}{arch_frequency}")
# add arch vendor with generation and hbm
for arch_vendor in arch_vendors:
    for arch_generation in arch_generations:
        for arch_frequency in arch_frequencies:
            archs.append(f"-{arch_vendor}{arch_generation}{arch_frequency}")


#########################################
# build gpus
#########################################
# add only gpu_modes with gpu_models
for gpu_mode in gpu_modes:
    for gpu_model in gpu_models:
        gpus.append(f"-{gpu_mode}{gpu_model['name']}")
# add gpu_modes with gpu_models and gpu_generations
for gpu_mode in gpu_modes:
    for gpu_model in gpu_models:
        for gpu_generation in gpu_model["generations"]:
            gpus.append(f"-{gpu_mode}{gpu_model['name']}{gpu_generation['name']}")
# add gpu_modes with gpu_models and comupte units. generate also entries with the gpu_generation
for gpu_mode in gpu_modes:
    for gpu_model in gpu_models:
        for gpu_generation in gpu_model["generations"]:
            for compute_units in gpu_generation['compute_units']:
                gpus.append(f"-{gpu_mode}{gpu_model['name']}{gpu_generation['name']}{compute_units}")
                gpus.append(f"-{gpu_mode}{gpu_model['name']}{compute_units}")
# add gpu_modes with gpu_models, comupte units and hbm. generate also entries with the gpu_generation
for gpu_mode in gpu_modes:
    for gpu_model in gpu_models:
        for gpu_generation in gpu_model["generations"]:
            for compute_units in gpu_generation['compute_units']:
                for gpu_hbm in gpu_hbms:
                    gpus.append(f"-{gpu_mode}{gpu_model['name']}{gpu_generation['name']}{compute_units}{gpu_hbm}")
                    gpus.append(f"-{gpu_mode}{gpu_model['name']}{compute_units}{gpu_hbm}")

#########################################
# build specials
#########################################
# since every combination is possible, build a powerset
specials = itertools.chain.from_iterable(
    itertools.combinations(special_list, r) for r in range(len(special_list) + 1)
)

#########################################
# build all possible SCS flavors
#########################################
for prefix in prefixes:
    for cpu in cpus:
        for ram in rams:
            for disk in disks:
                for virtualization in virtualizations:
                    for arch in archs:
                        for gpu in gpus:
                            for special in sepcials:
                                print(f"{prefix}{cpu}{ram}{disk}{virtualization}{arch}{gpu}{special}")
