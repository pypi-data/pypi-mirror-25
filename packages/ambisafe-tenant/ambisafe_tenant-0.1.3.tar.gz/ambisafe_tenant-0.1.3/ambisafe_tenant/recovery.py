import logging
import requests

from ambisafe_tenant import Crypt, AmbisafeTenantClient
from ambisafe_tenant.auth import SecondFactorAuth
from ambisafe_tenant.utils import remove_0x_from_address

logger = logging.getLogger('ambisafe_tenant')


class AmbisafeRecoveryClient(object):

    def __init__(self, tenant_sign_key, recovery_url, sf_api_key=None, sf_secret=None, cosign_protocol=False):
        self.tenant_sign_key = tenant_sign_key
        self.recovery_url = recovery_url
        self.sf_api_key = sf_api_key
        self.sf_secret = sf_secret
        self.cosign_protocol = cosign_protocol

    def recovery_setup_request(self, user_address, phone, email, user_recovery_id, use_phone_call=False):
        if not user_address.startswith('0x'):
            user_address = '0x' + user_address
        user_address_without_prefix = remove_0x_from_address(user_address)

        if use_phone_call:
            medium = 'call'
        else:
            medium = 'sms'

        if self.cosign_protocol:
            uri = 'customer/cosigning_protocol/create/'
            data = {
                      "userEthAddress": user_address,
                      "signupHexData": "0x00",
                      "phone": phone,
                      "email": email,
                      "via": medium,
                    }
        else:
            c = Crypt(user_address_without_prefix, self.tenant_sign_key)
            signature = c.get_recovery_tenant_signatures()
            uri = 'customer/create/'
            data = {
                  "address": user_address,
                  "phone": phone,
                  "email": email,
                  "via": medium,
                  "rTenant": signature.get('r'),
                  "sTenant": signature.get('s'),
                  "vTenant": signature.get('v'),
                  "nonceTenant": signature.get('nonce')
                }

        url = self.recovery_url + uri
        sf_data = {
          "language": "en-GB",
          "user_id": str(user_recovery_id)
        }
        data.update(sf_data)
        logger.debug('Secondfactor request data: {} to {}'.format(data, uri))
        response = self.make_request('POST', url, data, auth=SecondFactorAuth(self.sf_api_key,
                                                                              self.sf_secret,
                                                                              data, uri))
        return response

    def migration_request(self, user_address, phone, email, user_recovery_id, medium="sms"):
        if not user_address.startswith('0x'):
            user_address = '0x' + user_address

        uri = 'customer/cosigning_protocol/force_create/'
        data = {
                  "userEthAddress": user_address,
                  "signupHexData": "0x00",
                  "phone": phone,
                  "email": email,
                  "via": medium
                }
        url = self.recovery_url + uri
        sf_data = {
          "language": "en-GB",
          "user_id": str(user_recovery_id)
        }
        data.update(sf_data)
        logger.debug('Secondfactor migration data: {} to {}'.format(data, uri))
        response = self.make_request('POST', url, data, auth=SecondFactorAuth(self.sf_api_key,
                                                                              self.sf_secret,
                                                                              data, uri))
        return response

    def recovery_request(self, old_address, new_address, user_recovery_id, signupHexData=None, use_phone_call=False):
        if self.cosign_protocol:
            if use_phone_call:
                uri = 'customer/cosigning_protocol/call/'
            else:
                uri = 'customer/cosigning_protocol/sms/'
            if not signupHexData.startswith('0x'):
                signupHexData = '0x' + signupHexData
            data = {
                      "signupHexData": signupHexData,
                    }
        # Making recovery request for not cosign_protocol recovery
        else:
            if not old_address.startswith('0x'):
                old_address = '0x' + old_address
            if not new_address.startswith('0x'):
                new_address = '0x' + new_address

            sig_data = remove_0x_from_address(old_address) + remove_0x_from_address(new_address)
            c = Crypt(sig_data, self.tenant_sign_key)
            signature = c.get_recovery_tenant_signatures()
            data = {
              "oldAddr": old_address,
              "newAddr": new_address,
              "rTenant": signature.get('r'),
              "sTenant": signature.get('s'),
              "vTenant": signature.get('v'),
              "nonceTenant": signature.get('nonce'),
            }
            if use_phone_call:
                uri = "customer/call_recovery/"
            else:
                uri = "customer/sms_recovery/"
        url = self.recovery_url + uri
        sf_data = {
          "user_id": str(user_recovery_id)
        }
        data.update(sf_data)
        logger.debug('Secondfactor recovery request data: {} to {}'.format(data, uri))
        response = self.make_request('POST', url, data, auth=SecondFactorAuth(self.sf_api_key,
                                                                              self.sf_secret,
                                                                              data,
                                                                              uri))
        return response

    def recovery_setup_confirmation(self, code, request_id, user_recovery_id=None):
        data = {
            "code": code,
            "user_id": str(user_recovery_id)
        }
        if self.cosign_protocol:
            uri = 'customer/cosigning_protocol/confirm/'
            cosign_data = {
                'makenoise_id': str(request_id)
            }
            data.update(cosign_data)
        else:
            uri = 'customer/confirm/'
        url = self.recovery_url + uri
        auth = SecondFactorAuth(self.sf_api_key, self.sf_secret, data, uri)
        response = self.make_request('POST', url, data, auth)
        return response

    def update_phone_number_request(self, user_recovery_id, new_phone, use_phone_call=False):
        uri = 'customer/update_phone_number/'
        url = self.recovery_url + uri
        via = 'sms' if not use_phone_call else 'call'
        data = {
            'new_phone': new_phone,
            'via': via,
            'user_id': user_recovery_id
        }
        logger.debug('Secondfactor update phone number request with data: {}'.format(data))
        auth = SecondFactorAuth(self.sf_api_key, self.sf_secret, data, uri)
        return self.make_request('POST', url, data, auth=auth)

    def update_phone_number_confirm(self, user_recovery_id, code, makenoise_id):
        uri = 'customer/confirm_update_phone_number/'
        url = self.recovery_url + uri
        data = {
            'user_id': user_recovery_id,
            'makenoise_id': makenoise_id,
            'code': code
        }
        logger.debug('Secondfactor update phone number confirm with data: {}'.format(data))
        auth = SecondFactorAuth(self.sf_api_key, self.sf_secret, data, uri)
        return self.make_request('POST', url, data, auth=auth)

    def make_request(self, method, url, body=None, auth=None):
        headers = {u'Accept': u'application/json'}
        logger.debug('Ambisafe-tenant lib, make-request body: {}'.format(body))
        logger.debug('Ambisafe-tenant lib, make-request url: {}'.format(url))
        response = requests.request(method, url, headers=headers, json=body, auth=auth)
        logger.debug(response.text)
        return AmbisafeTenantClient._handle_response(response)
