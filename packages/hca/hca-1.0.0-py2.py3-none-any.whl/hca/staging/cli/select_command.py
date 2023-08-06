import re

import tweak

import hca


class StagingAreaURN:
    def __init__(self, urn):
        self.urn = urn
        urnbits = urn.split(':')
        if len(urnbits) == 5:  # production URN hca:sta:aws:uuid:creds
            self.uuid = urnbits[3]
        elif len(urnbits) == 6:  # non-production URN hca:sta:aws:stage:uuid:creds
            self.uuid = urnbits[4]
        else:
            raise RuntimeError("Bad URN: %s" % (urn,))


class SelectCommand:

    def __init__(self, args):
        self.config = self._load_config()
        if re.search(':', args.urn_or_alias):  # URN
            self._save_and_select_area_by_urn(args.urn_or_alias)
        else:  # alias
            self._select_area_by_alias(args.urn_or_alias)
        self.config.save()

    def _save_and_select_area_by_urn(self, urn_string):
        urn = StagingAreaURN(urn_string)
        if urn.urn not in self.config.staging.areas:
            self.config.staging.areas[urn.uuid] = urn.urn
        self._select_area(urn.uuid)

    def _select_area_by_alias(self, alias):
        matching_areas = [uuid for uuid in self.config.staging.areas if re.match(alias, uuid)]
        if len(matching_areas) == 0:
            print("Sorry I don't recognize area \"%s\"" % (alias,))
        elif len(matching_areas) == 1:
            self._select_area(matching_areas[0])
        else:
            print("\"%s\" matches more than one area, please provide more characters." % (alias,))

    def _select_area(self, area_uuid):
        self.config.staging.current_area = area_uuid
        print("Staging area %s selected." % area_uuid)
        print("You may refer to this staging area in future using the first few characters, e.g. \"%s\"" %
              area_uuid[0:3])

    @staticmethod
    def _load_config():
        config = tweak.Config(hca.TWEAK_PROJECT_NAME)
        if 'staging' not in config:
            config.staging = {}
        if 'areas' not in config.staging:
            config.staging.areas = {}
        return config
