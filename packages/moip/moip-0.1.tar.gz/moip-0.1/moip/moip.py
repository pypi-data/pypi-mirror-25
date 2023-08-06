import json
from copy import copy

import requests

from .response import Response


class Moip(object):
    def __init__(self):
        self.base_url = None
        self.environment = None
        self.key = None
        self.token = None

    def get_environments(self):
        return 'production', 'sandbox'

    def set_environment(self, environment):
        environments = self.get_environments()
        if environment not in environments:
            raise ValueError(
                'Invalid environment. Must be one of: {0}'.format(
                    ', '.join(environments)
                )
            )

        moip = copy(self)

        if environment == 'production':
            moip.base_url = 'https://api.moip.com.br'
        elif environment == 'sandbox':
            moip.base_url = 'https://sandbox.moip.com.br'

        moip.environment = environment

        return moip

    def set_key(self, key):
        moip = copy(self)
        moip.key = key
        return moip

    def set_token(self, token):
        moip = copy(self)
        moip.token = token
        return moip

    def get(self, url, parameters=None):
        response = requests.get('{0}/{1}'.format(self.base_url, url),
                                params=parameters,
                                auth=(self.token, self.key))

        return Response(response.status_code,
                        False,
                        json.loads(response.text))

    def post(self, url, parameters=None):
        headers = {
            'Content-type': 'application/json; charset="UTF-8"',
        }

        response = requests.post('{0}/{1}'.format(self.base_url, url),
                                 data=json.dumps(parameters),
                                 headers=headers,
                                 auth=(self.token, self.key))

        return Response(response.status_code,
                        False,
                        json.loads(response.text))

    def post_customer(self, parameters):
        response = self.post('v2/customers', parameters=parameters)
        return Response(response.status,
                        response.status == 201,
                        response.content)

    def get_customer(self, customer_id):
        response = self.get('v2/customers/{0}'.format(customer_id))
        return Response(response.status,
                        response.status == 200,
                        response.content)

    def post_creditcard(self, customer_id, parameters):
        response = self.post(
            'v2/customers/{0}/fundinginstruments'.format(customer_id),
            parameters=parameters
        )

        if response.status == 201:
            return Response(201, True, {'id': response['creditCard']['id']})
        else:
            return Response(response.status, False, response.content)

    def delete_creditcard(self, creditcard_id):
        response = requests.delete(
            '{0}/v2/fundinginstruments/{1}'.format(self.base_url,
                                                   creditcard_id),
            auth=(self.token, self.key)
        )

        return Response(response.status_code,
                        response.status_code == 200)

    def post_order(self, parameters):
        response = self.post('v2/orders', parameters=parameters)

        if response.status == 201:
            return Response(201, True, response.content)
        else:
            return Response(response.status, False, response.content)

    def get_order(self, order_id):
        try:
            response = self.get('v2/orders/{0}'.format(order_id))
        except json.decoder.JSONDecodeError:
            # patching Moip's API, as it actually returns an HTTP 200 for
            # 'Not found'
            return Response(404, False)

        if response.status == 200:
            return Response(200, True, response.content)
        else:
            return Response(response.status, False, response.content)

    def post_payment(self, order_id, parameters):
        response = self.post('v2/orders/{0}/payments'.format(order_id),
                             parameters)
        return Response(response.status,
                        response.status == 201,
                        response.content)

    def get_payment(self, payment_id):
        response = self.get('v2/payments/{0}'.format(payment_id))
        return Response(response.status,
                        response.status == 200,
                        response.content)

    def capture_payment(self, payment_id):
        try:
            response = self.post('v2/payments/{0}/capture'.format(payment_id))
        except json.decoder.JSONDecodeError:
            # patching Moip's API, as it actually returns an HTTP 200 for
            # 'Not found'
            return Response(404, False)

        return Response(response.status,
                        response.status == 200,
                        response.content)

    def void_payment(self, payment_id):
        try:
            response = self.post('v2/payments/{0}/void'.format(payment_id))
        except json.decoder.JSONDecodeError:
            # patching Moip's API, as it actually returns an HTTP 200 for
            # 'Not found'
            return Response(404, False)

        return Response(response.status,
                        response.status == 200,
                        response.content)

    def account_exists(self, account_id):
        try:
            return self.get('v2/accounts/{0}'.format(account_id)).status == 200
        except json.JSONDecodeError:
            return False
