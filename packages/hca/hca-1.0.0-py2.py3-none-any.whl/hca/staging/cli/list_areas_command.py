import tweak

import hca


class ListAreasCommand:

    def __init__(self, args):
        config = self._load_config()
        for uuid in config.staging.areas:
            print(uuid)

    @staticmethod
    def _load_config():
        config = tweak.Config(hca.TWEAK_PROJECT_NAME)
        if 'staging' not in config:
            config.staging = {}
        if 'areas' not in config.staging:
            config.staging.areas = {}
        return config
