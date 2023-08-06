import logging
import time
import requests
from account import Account
from ambisafe_tenant.auth import AmbisafeTenantAuth
from ambisafe_tenant.exc import ServerError, ClientError

logger = logging.getLogger('ambisafe_tenant')


class AmbisafeTenantClient(object):
    def __init__(self, api_key, api_secret, keystorage_server_url=None, faucet_oracle_url=None, notificator_url=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.keystorage_server_url = keystorage_server_url
        self.faucet_oracle_url = faucet_oracle_url
        self.notificator_url = notificator_url

    def save_account_to_keystore(self, user_uuid, address, container):
        if not self.keystorage_server_url:
            raise ClientError('Validation Error', 'KeyStorage url is not provided')
        uri = '/keystore/{}'.format(user_uuid)
        url = self.keystorage_server_url + uri
        data = {
            'crypto': container,
            'address': address,
            'id': str(user_uuid),
            'version': 0
        }
        response = self.make_request('POST', url, body=data, resource='storage')
        return response

    def get_account(self, user_uuid):
        if not self.keystorage_server_url:
            raise ClientError('Validation Error', 'KeyStorage url is not provided')
        uri = '/keystore/{}'.format(user_uuid)
        url = self.keystorage_server_url + uri
        account_data = self.make_request('GET', url)
        return Account(**account_data)

    def topup_account(self, address, amount):
        if not self.faucet_oracle_url:
            raise ClientError('Validation Error', 'Faucet Oracle url is not provided')
        if not address.startswith('0x'):
            address = '0x' + address
        data = {
            "to": address,
            "amount": amount
        }
        response = self.make_request('POST', self.faucet_oracle_url, data, 'faucet')
        return response

    def reparse_blocks(self, block_numbers):
        if not self.notificator_url:
            raise AssertionError('`notificator_url` setting is not set')
        data = {
            "block_numbers": block_numbers
        }
        response = self.make_request('POST', self.notificator_url, data, 'notificator-reparse')
        return response

    def make_invoice_for_udr(self, service_name, udr_url):
        data = {
            "subscriptionId": self.api_key,
            "subject": service_name,
            "timestamp": int(time.time() * 1000)
        }
        response = self.make_request('POST', udr_url, data, 'faucet')
        return response

    def reserve_user_contract(self, assign_service_url, address, email, external_id):
        uri = '/assign/'
        url = assign_service_url + uri
        data = {
            'address': address,
            'email': email,
            'external_id': str(external_id)
        }
        response = self.make_request('POST', url, data, 'assigner')
        return response

    def user_contract_is_assigned(self, assign_service_url, address):
        uri = '/is_assigned/'
        url = assign_service_url + uri
        data = {
            'address': address,
        }
        response = self.make_request('POST', url, data, 'assigner')
        return response

    def get_user_contract_by_email(self, assign_service_url, email):
        uri = '/get/usercontract/{}/'.format(email)
        url = assign_service_url + uri
        response = self.make_request('GET', url, resource='assigner')
        return response

    def sign_data_with_oracle(self, assign_service_url, data, user_contract_address, nonce, cosigner=None):
        uri = '/oracle/sign/'
        url = assign_service_url + uri
        data = {
            'data': data,
            'user_address': user_contract_address,
            'nonce': nonce,
        }
        if cosigner:
            data.update({'cosigner': cosigner})
        response = self.make_request('POST', url, data, 'assigner')
        return response

    def update_assigned_address(self, assign_service_url, email, address):
        uri = '/update/address/'
        url = assign_service_url + uri
        data = {
            'email': email,
            'address': address
        }
        response = self.make_request('POST', url, data, 'assigner')
        return response

    def get_assigner_billing_data(self, assign_service_url):
        uri = '/billing/info/'
        url = assign_service_url + uri
        response = self.make_request('GET', url, resource='assigner')
        return response

    def make_request(self, method, url, body=None, resource=None):
        headers = {u'Accept': u'application/json'}
        if resource:
            token = AmbisafeTenantAuth(self.api_key, self.api_secret, resource).get_jws_token()
            headers[u'Authorization'] = token
        response = requests.request(method, url, headers=headers, json=body)
        return AmbisafeTenantClient._handle_response(response)

    @staticmethod
    def validate_jws_token(token, url):
        if not url.endswith('/'):
            url += '/'
        url = url + token
        response = requests.get(url)
        return AmbisafeTenantClient._handle_response(response)

    @staticmethod
    def _handle_response(response):
        logger.debug(response.text)
        try:
            response_data = response.json()
            logger.debug(response_data)
        except ValueError as e:
            # ValueError is parent of JSONDecodeError
            raise ServerError(e.message, 'Bad Response')
        if not response.ok:
            if response.status_code == 402:
                raise ClientError('BillingError', 'BillingError')
            if 400 <= response.status_code < 500:
                raise ClientError(response_data.get('errorMessage', response_data.get('message',
                                                                                      response_data.get('error'))),
                                  response_data.get('errorMessage', response_data.get('message',
                                                                                      response_data.get('error')))
                                  )
            elif 500 <= response.status_code < 600:
                raise ServerError(response_data.get('errorMessage', response_data.get('message',
                                                                                      response_data.get('error'))),
                                  response_data.get('errorMessage', response_data.get('message',
                                                                                      response_data.get('error')))
                                  )
        return response_data
