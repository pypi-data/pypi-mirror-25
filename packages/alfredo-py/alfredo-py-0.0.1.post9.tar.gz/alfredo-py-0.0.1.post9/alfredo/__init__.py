import sys

import ruamel.yaml as yaml

from alfredo import descriptions
from alfredo.resource import HttpPropertyResource

__version__ = '0.0.1.post9'


def represent_unicode(self, data):
    return self.represent_str(data.encode('utf-8'))


if sys.version_info < (3,):
    yaml.representer.Representer.add_representer(unicode, represent_unicode)


def ruote(token=None):
    root = HttpPropertyResource(None, 'https://preapi.teamjamon.com', descriptions.ruote)
    if token is not None:
        root.headers = dict(Authorization="Token %s" % token)
    return root


def virgo():
    return HttpPropertyResource(None, 'https://virgo.teamjamon.com', descriptions.virgo)
