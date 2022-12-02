# https://github.com/SovereignCloudStack/Docs/blob/main/Design-Docs/flavor-naming.md

# Examples of some valid flavors:
# SCS-1L:1
# SCS-16V:32:100
# SCSX-1V:0.5:
# SCSX-1V:0.5:n
# SCSX-128Ti-16x16000h-bms-hwv-z3hhh-GNa:128hhh-ib


def check_prefix(item: str) -> bool:
    if item.startswith("SCS-"):
        return True
    elif item.startswith("SCSX-"):
        return True
    else:
        return False


def check_cpu(item: str) -> bool:
    # strip away unnecessary string parts
    item = item.split(':')[0].split('-')[1]
    # remaining possible values: 1L, 16V, 128Ti

    # check, if there is no decimal number included:
    if "." in item:
        return False

    # split numbers and suffixes
    suffix = item.lstrip('0123456789')
    core_count = item[:len(suffix) + 1]

    # check if there is at least one number and not null
    if not core_count.isdigit():
        return False
    if int(core_count) == 0:
        return False

    # check for and remove "i"
    if "i" in suffix:
        if suffix[-1:] != "i":
            return False
        suffix = suffix[:-1]

    # check for length of suffix
    if len(suffix) != 1:
        return False

    # check for valid suffix letters
    if suffix not in "LVTC":
        return False

    return True


def check_ram(item: str) -> bool:
    # strip away unnecessary string parts
    item = item.split(':')[1]
    # remaining possible values: 1L, 16V, 128Ti
    pass


def scs_naming_is_valid(item: str) -> bool:
    check_list = []
    check_list.append(check_prefix(item))
    check_list.append(check_cpu(item))
    check_list.append(check_ram(item))
    # check_list.append(check_disk(item))
    # check_list.append(check_disk_type(item))
    # check_list.append(check_extra_features(item))

    if False in check_list:
        return False
    else:
        return True


print(scs_naming_is_valid("SCSX-128Ti-16x16000h-bms-hwv-z3hhh-GNa:128hhh-ib"))
