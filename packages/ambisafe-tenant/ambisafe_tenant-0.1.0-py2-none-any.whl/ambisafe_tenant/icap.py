import random
import string
from stdnum import iban
from stdnum.iso7064 import mod_97_10


class IcapAddress(object):
    def __init__(self, icap_asset, institution_name):
        self.icap_asset = icap_asset
        self.institution_name = institution_name
        self.country_code = 'XE'
        self.initial_checksum = '00'

    def generate_client_part(self):
        return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(9))

    def prepare_iban(self, iban_address):
        return iban._to_base10(iban_address)

    def generate_checksum(self, prepared_iban):
        checksum =  98 - mod_97_10.checksum(prepared_iban)
        return string.zfill(str(checksum), 2)

    def checksumed_icap(self):
        bban = self.icap_asset + self.institution_name + self.generate_client_part()
        no_checksumed_iban = self.country_code + self.initial_checksum + bban
        check_sum = self.generate_checksum(self.prepare_iban(no_checksumed_iban))
        iban = self.country_code + check_sum + bban
        return iban

