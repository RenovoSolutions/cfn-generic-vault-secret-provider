import requests
import json
import os
from copy import copy

class VaultLib():
    # Vault returns 204 when the endpoint has no response body
    # For example secret version deletion returns 204
    # See https://www.vaultproject.io/api#http-status-codes
    allowed_status_codes = [200, 204]

    def __init__(self, model, server, token, log):
        self.log = log
        log.info(f'Model is: {model}')
        log.info(f'Server is: {server}')
        self.model = copy(model)
        self.server = server
        self.auth = VaultLib.auth(token)

    def write_secret(self, secret_data):
        request_url = f'{self.server}/v1/{self.model.SecretEngineMountPath}/data/{self.model.SecretPath}'
        
        self.log.info(f'Writing secret: {request_url}')

        prepared_secret_data = dict(item.strip("'").split("=") for item in secret_data.split("', '"))

        secret_payload = {
            "data": prepared_secret_data
        }

        # local debug only
        # self.log.info(f'Will create secrets: {json.dumps(secret_payload)}')

        response = requests.post(request_url, data=json.dumps(secret_payload), headers=self.auth)

        if not response.status_code in VaultLib.allowed_status_codes:
            VaultLib.error_helper(self, response, 'write')
        else:
            self.log.info(f'Wrote secret: {response.status_code} {response.reason} {response.text}')

        return response

    def delete_secret_version(self, version):
        data = {
            "versions": [version]
        }

        request_url = f'{self.server}/v1/{self.model.SecretEngineMountPath}/delete/{self.model.SecretPath}'

        self.log.info(f'Deleting secret version {version}: {request_url}')

        response = requests.post(request_url, data=json.dumps(data), headers=self.auth)

        if not response.status_code in VaultLib.allowed_status_codes:
            VaultLib.error_helper(self, response, 'delete')
        else:
            self.log.info(f'Deleted secret: {response.status_code} {response.reason} {response.text}')

        return response

    def read_secret_version(self, version):
        request_url = f'{self.server}/v1/{self.model.SecretEngineMountPath}/data/{self.model.SecretPath}?version={version}'

        self.log.info(f'Reading secret version {version}: {request_url}')

        response = requests.get(request_url, headers=self.auth)

        if not response.status_code in VaultLib.allowed_status_codes:
            VaultLib.error_helper(self, response, 'read')
        else:
            self.log.info(f'Read secret: {response.status_code} {response.reason}')

        return response

    def error_helper(self, response, action):
        if response.status_code == 403:
            capabilities = VaultLib.check_token_capabilities(self, action)
            raise Exception(f'403 Forbidden. You cannot {action} secret {self.model.SecretPath} you only have the following capabilities: {capabilities}')
        if response.status_code == 404:
            if response.json()['data']['data'] == None:
                return response
        elif response.status_code == 503:
            raise Exception(f'503 Vault is down for maintenance or might be sealed.')
        else:
            raise Exception(f'Could not {action} secret: {response.status_code} {response.reason} {response.text}.')

    def auth(token=None):
        headers = {}

        if not token == None:
            headers = {'X-Vault-Token': token}
        else:
            # just a filler so requests doesn't error when using lambda plugin for vault
            headers = {'X-No-Token': 'NoToken'}

        return headers

    def check_token_capabilities(self, action):
        action_path = 'data'
        if action == 'delete':
            action_path = 'delete'

        data = {
            "paths": f"{self.model.SecretEngineMountPath}/{action_path}/{self.model.SecretPath}"
        }

        response = requests.post(f'{self.server}/v1/sys/capabilities-self', data=json.dumps(data), headers=self.auth)

        return response.json()['capabilities']
