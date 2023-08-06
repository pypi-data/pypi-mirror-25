#
# Copyright (c) 2016 BlueData Software, Inc.
#
"""Module for building docker image for the current catalog.
"""
from __future__ import print_function
import os
import subprocess

from .image_file import OS_CLASS_DICT
from .. import SubCommand
from ..inmem_store import ENTRY_DICT, DELIVERABLE_DICT
from ..utils.misc import getOrgname, doSkipImageRebuild, buildingRegistryImage, getBaseOSMajorVersion
from ..utils.config import KEY_SDKBASE, KEY_STAGEDIR, SECTION_WB



DIRNAME = os.path.dirname(os.path.realpath(__file__))
SCRIPT_PATH = os.path.abspath(os.path.join(DIRNAME, '..', '..', 'build', 'image',
                                           'image_snapshot.sh'))
def runImageSnapShotScript(scriptParams):
    try:
        rc = subprocess.check_call(' '.join(scriptParams), shell=True,
                                   stderr=subprocess.STDOUT)
        return rc == 0
    except subprocess.CalledProcessError as cpe:
        print(cpe)
        return False

def validateOSForContentTrustOperations():
    if int(getBaseOSMajorVersion()) >= 7:
        return True
    print("ERROR: Content Trust operations only available for CentOS/RHEL 7.x or greater platforms.")
    return False

class ImageBuild(SubCommand):
    """
    Subcommand for building docker image for the catalog
    """
    def __init__(self, config, inmemStore, cmdObj):
        SubCommand.__init__(self, config, inmemStore, cmdObj, 'build')
        self.imageRegistryUrl = None

    def __prepareImageFeedMetadata(self, pargs):
        metadata = {}
        metadata['image_name'] = self.__constructNametagForImage(pargs)
        metadata['registry_url'] = self.imageRegistryUrl
        metadata['registry_auth_enabled'] = \
        self.inmemStore.getDict(DELIVERABLE_DICT)['registry_auth_enabled']
        metadata['content_trust_enabled'] = pargs.contentTrustEnabled
        return metadata

    def __buildRegistryImage(self, pargs):
        imageFeedMetadata = self.__prepareImageFeedMetadata(pargs)
        self.inmemStore.addField(ENTRY_DICT, "image", imageFeedMetadata)
        self.inmemStore.addField(DELIVERABLE_DICT, "imageOS", OS_CLASS_DICT[pargs.os][0])
        self.inmemStore.addField(DELIVERABLE_DICT, "imageOSMajor", OS_CLASS_DICT[pargs.os][1])
        return self.__dockerBuildAndPushImageToRegistry(imageFeedMetadata, pargs)

    def __dockerBuildAndPushImageToRegistry(self, imageMetadata, pargs):

        sdkBase = self.config.get(SECTION_WB, KEY_SDKBASE)
        scriptPath = os.path.join(sdkBase, "appbuild", "image", "image_snapshot.sh")
        absBaseDir = os.path.abspath(pargs.basedir)
        if not os.path.exists(absBaseDir):
            print("ERROR: '%s' does not exist.")
            return False
        scriptParams = ["bash", scriptPath,
                        "--basedir", absBaseDir,
                        "--nametag", imageMetadata["image_name"],
                        "--registry", self.imageRegistryUrl,
                        "--baseos", getBaseOSMajorVersion()]
        if pargs.contentTrustEnabled:
            scriptParams.append("--trust")
        if imageMetadata['registry_auth_enabled']:
            scriptParams.append("--registry-auth-enabled")
        return runImageSnapShotScript(scriptParams)

    def __constructNametagForImage(self, pargs):
        if pargs.distroid is None:
            entryDict = self.inmemStore.getDict(ENTRY_DICT)
            if entryDict.has_key('distro_id'):
                distroid = entryDict['distro_id']
            else:
                print ("ERROR: Either -d/--distroid must be specified or a "
                       "catalog entry with a valid distroid specification "
                       "must be loaded.")
                return False
        else:
            orgname = getOrgname(self.inmemStore, self.config)
            if orgname is None:
                return False
            distroid = "%s/%s" % (orgname, pargs.distroid)

        if self.imageRegistryUrl is None or self.imageRegistryUrl == "default":
            return "%s-%s:%s" %(distroid, pargs.os, pargs.version)

        return "%s/%s-%s:%s" %(self.imageRegistryUrl, distroid, pargs.os, pargs.version)



    def getSubcmdDescripton(self):
        return 'Build a catalog image from a Dockerfile.'

    def populateParserArgs(self, subparser):
        subparser.add_argument('-b', '--basedir', metavar='BASEDIR', type=str,
                               required=True, action="store",
                               help='Directory path where the Dockerfile and '
                                    'related files are located.')
        subparser.add_argument('-d', '--distroid', metavar='DISTRO_ID', type=str,
                               required=False, action='store', default=None,
                               help="EPIC catalog entry's distro id to which this "
                               "image will be assigned to. If a catalog entry "
                               "is either loaded or is being created in the "
                               "current workbench session, this option is not "
                               "required.")
        subparser.add_argument('-v', '--imgversion', metavar='IMAGE_VERSION',
                               type=str, dest='version', required=True,
                               help='Container Image version in the form of a '
                                    '"major.minor" string.')
        subparser.add_argument('--os', metavar="OS", dest="os", required=True,
                               choices=['centos6', 'rhel6', 'centos7', 'rhel7',
                                        'ubuntu16'], action='store',
                               help="The OS distribution of the container image.")
        subparser.add_argument('--trust', dest="contentTrustEnabled", required=False,
                               action="store_true",
                               help="Build this image with Docker Content Trust enabled."
                               "Only applicable "
                               "for OS choices of rhel7, centos7 and ubuntu16")

    def run(self, pargs):
        self.imageRegistryUrl = buildingRegistryImage(self.inmemStore)
        if self.imageRegistryUrl is not None and pargs.contentTrustEnabled:
            return validateOSForContentTrustOperations() and self.__buildRegistryImage(pargs)
        elif self.imageRegistryUrl is not None:
            return self.__buildRegistryImage(pargs)
        else:
            stagingDir = self.config.get(SECTION_WB, KEY_STAGEDIR)
            sdkBase = self.config.get(SECTION_WB, KEY_SDKBASE)
            scriptPath = os.path.join(sdkBase, "appbuild", "image", "image_snapshot.sh")

            if not os.path.exists(stagingDir):
                os.makedirs(stagingDir)

            absBaseDir = os.path.abspath(pargs.basedir)
            if not os.path.exists(absBaseDir):
                print("ERROR: '%s' does not exist.")
                return False

            ## Construct the nametag options for building it. We need three pieces
            ## for that: orgname/distroid:version

            nametag = self.__constructNametagForImage(pargs)
            self.inmemStore.addField(DELIVERABLE_DICT, "imageName", nametag)
            destFilename = nametag.replace('/', '-').replace(':', '-')
            destPath = os.path.join(stagingDir, "%s%s" % (destFilename, ".tar.gz"))
            md5File = destPath + '.md5sum'

            if not doSkipImageRebuild(destPath, md5File):
                scriptParams = ["bash", scriptPath,
                                "--basedir", absBaseDir,
                                "--nametag", nametag,
                                "--filename", destPath]

                runImageSnapShotScript(scriptParams)

            try:
                with open(md5File, 'r') as mf:
                    md5 = mf.readline().split()[0]

                return self.workbench.onecmd(str("image file --filepath %s --md5sum %s --os %s"
                                                 %(destPath, md5, pargs.os)))
            except IOError:
                return self.workbench.onecmd(str("image file --filepath %s --os %s"
                                                 %(destPath, pargs.os)))

            return True

    def complete(self, text, argsList):
        return []
