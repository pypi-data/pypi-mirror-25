from copy import copy


def remove_0x_from_address(address):
    address = copy(address)
    if address.startswith('0x'):
        address = address[2:]
    return address