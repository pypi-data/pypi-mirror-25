import os
from typing import List

import yaml


class Object():
    pass

class ObjectFactory():

    def __init__(self, d:dict):
        self.d = d

    def create(self):
        obj = Object()
        for k, v in self.d.items():
            if isinstance(v, dict):
                obj.__dict__[k] = ObjectFactory(v).create()
            else:
                obj.__dict__[k] = v
        return obj


class SettingsObjectFactory():

    def __init__(self, settings:dict):
        self.settings = settings

    def get_settings(self, env:str):
        env_settings = self.settings.get('common', {})
        env_settings.update(self.settings[env])
        return ObjectFactory(env_settings).create()


def create(env:str, settings:str, secrets:dict=None):
    """
    Creates setting object, which has properties from the settings file.
    secrets dict can contain environment specific secrets, which are updated to
    settings.
    """
    with open(settings, 'rt') as f:
        settings_data = yaml.load(f.read())
    if secrets and env in secrets:
        with open(secrets[env], 'rt') as f:
            secret_data = yaml.load(f.read())
        settings_data[env].update(secret_data)

    return SettingsObjectFactory(settings_data).get_settings(env)


