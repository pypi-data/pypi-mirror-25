#
# Copyright (c) 2017 BlueData Software, Inc.
#

"""
Subcommand to \"builder\" main command for specifying registry details.
"""

from __future__ import print_function
from .. import SubCommand
from ..inmem_store import DELIVERABLE_DICT

class BuilderRegistry(SubCommand):
    """
    Subcommand to \"builder\" main command for specifying registry details.
    """

    def __init__(self, config, inmemStore, cmdObj):
        SubCommand.__init__(self, config, inmemStore, cmdObj, 'registry')


    def getSubcmdDescripton(self):
        return 'Set the registry URL for this catalog entry. For privately hosted ' +\
              'registries, the convention is \"registry-host:port\". For ' +\
              'Docker Hub, the value is \"default\". For other registries, ' +\
              'the value will be the URL of the registry without http or https prefix.'


    def populateParserArgs(self, subparser):
        subparser.add_argument('-u', '--url', dest='registryUrl', nargs='?',
                               required=False, default='default', const='default',
                               metavar="registry-host:port or HTTP URL without http prefix",
                               help='Registry URL for the image. ' + \
                               'In case of Docker Hub, no value needed.')
        subparser.add_argument('--auth-enabled', dest='registryAuthEnabled', required=False,
                               action='store_true', help='Whether this registry requires authentication.')
        return

    def run(self, pargs):
        if pargs.registryUrl is not None and ' ' in pargs.registryUrl:
            print("ERROR: No space is allowed in the registry url.")
            return False

        self.inmemStore.addField(DELIVERABLE_DICT, "registry_url", pargs.registryUrl.strip().lower())
        self.inmemStore.addField(DELIVERABLE_DICT, "registry_auth_enabled", pargs.registryAuthEnabled)
        return True

    def complete(self, text, argsList):
        return []
