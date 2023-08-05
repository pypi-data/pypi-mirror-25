from __future__ import absolute_import, print_function, unicode_literals

import os
import json
import click

from cryptography.fernet import Fernet


class Secrets(object):

    def encrypt(self, config, env):
        encrypt_key = os.environ.get('DOJO_DECRYPT_KEY')
        if not encrypt_key and click.confirm('No key found in your environment variables. Would you like to generate a key?'):
            encrypt_key = Fernet.generate_key()
            click.echo(click.style('Your Key: %s (keep this safe)', fg='red', bold=True) % encrypt_key)
        env_json_secrets_path = os.path.join(config, 'secrets.%s.json' % (env, ))
        env_json_secrets = self._read_file(env_json_secrets_path)
        if not env_json_secrets:
            raise ValueError('File %s does not exist or is empty.' % env_json_secrets_path)
        else:
            fernet = Fernet(encrypt_key)
            token = fernet.encrypt(env_json_secrets)
            with open(env_json_secrets_path + '.enc', 'w') as encrypted_file:
                encrypted_file.write(token)
        return encrypted_file

    def decrypt(self, json_secrets_path):
        encrypt_key = os.environ.get('DOJO_DECRYPT_KEY')
        if not encrypt_key or not json_secrets_path:
            raise ValueError('Missing a requirement for decrypting. Secrets path or DOJO_DECRYPT_KEY.')
        secrets_file = self._read_file(json_secrets_path)

        # If there aren't any encrypted files, try loading the unecrypted file instead
        if os.path.isfile(json_secrets_path.split('.enc')[0]) and not os.path.isfile(json_secrets_path):
            try:
                secrets = json.loads(open(json_secrets_path.split('.enc')[0]).read())
            except ValueError as e:
                raise ValueError(e)
        else:
            try:
                fernet = Fernet(encrypt_key)
                out = fernet.decrypt(secrets_file.encode())
            # TODO proper error handling? https://cryptography.io/en/latest/fernet/#cryptography.fernet.Fernet.decrypt
            except ValueError as e:
                raise ValueError(e)
            try:
                secrets = json.loads(out)
            except ValueError as e:
                raise ValueError(e, out)

        return secrets

    def _read_file(self, path):
        if os.path.isfile(path):
            with open(path, 'r') as f:
                return f.read()
        else:
            return {}
