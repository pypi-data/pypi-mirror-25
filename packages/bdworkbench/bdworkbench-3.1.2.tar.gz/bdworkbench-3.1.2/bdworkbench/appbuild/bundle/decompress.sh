#!/bin/bash
#
# Copyright (c) 2016, BlueData Software, Inc.
#set -x
set -o pipefail

OSNAME=$(uname -s)

END='\033[0m'
BOLD='\033[1m'

BUILD_TYPE="@@@@BUILDTYPE@@@@"
BUNDLE_NAME="@@@@BUNDLENAME@@@@"
TAR_FILE_CSUM="@@@@TARFILECHECKSUM@@@@"
TAR_ENTRY_JSON='@@@@TARENTRYJSON@@@@'
TAR_ENTRY_SETUP='@@@@TARENTRYSETUP@@@@'
TAR_ENTRY_IMAGE='@@@@TARENTRYIMAGE@@@@'
SRC_PACKAGE_NAME='@@@SOURCEPACKAGE@@@'
REGISTRY_AUTH_ENABLED='@@@REGISTRY_AUTH_ENABLED@@@'

# Allow the extraction directory to be overridden through an env variable.
if [[ -z ${EXTRACT_BASE_DIR} ]]; then
    EXTRACT_BASE_DIR="@@@@TAREXTRACTDIR@@@@/${BUNDLE_NAME}"
else
    EXTRACT_BASE_DIR="${EXTRACT_BASE_DIR}/${BUNDLE_NAME}"
fi

ENTRY_JSON_PATH="${EXTRACT_BASE_DIR}/${TAR_ENTRY_JSON}"

if [[ "${TAR_ENTRY_SETUP}" != 'undefined' ]]; then
    ENTRY_SETUP_PATH="${EXTRACT_BASE_DIR}/${TAR_ENTRY_SETUP}"
fi

if [[ "${TAR_ENTRY_IMAGE}" != 'undefined' ]]; then
    ENTRY_IMAGE_PATH="${EXTRACT_BASE_DIR}/${TAR_ENTRY_IMAGE}"
fi

FEED='false'
FILES='false'
PAYLOAD='false'
VERIFY_ONLY='false'
EXTRACT_ONLY='false'
EXTRACT_SOURCES='false'
CHCON_BIN="$(which chcon)"

SELF="$0"
###############################################################################
# Calculate the offset of the archive contents.                               #
###############################################################################
ARCHIVE_OFFSET=''
get_archive_offset() {
    if [ "$ARCHIVE_OFFSET" == '' ]; then
        ARCHIVE_OFFSET=`awk '/^__ARCHIVE__/ {print NR + 1; exit 0; }' $SELF`
    fi

    echo $ARCHIVE_OFFSET
}

###############################################################################
# Verify that the checksum stored in the script matches that of the archive.  #
###############################################################################
verify() {
    echo -n "Checking integrity ... "

    if [[ "${OSNAME}" == 'Linux' ]]; then
        CHECKSUM=$(tail -n+$(get_archive_offset) $SELF | md5sum | awk '{print $1}')
    elif [[ "${OSNAME}" == 'Darwin' ]]; then
        CHECKSUM=$(tail -n+$(get_archive_offset) $SELF | md5 | awk '{print $NF}')
    else
        echo "UNKNOWN OS ('${OSNAME}')."
        exit 2
    fi

    if [ "$CHECKSUM" != "$TAR_FILE_CSUM" ]; then
        echo "BAD."
        echo "ERROR: Bundle integrity check failed. Expected: ${TAR_FILE_CSUM} Got: $CHECKSUM"
        exit 2
    fi
    echo "GOOD."
}

################################################################################
# Erases or deletes all the files installed by this catalog bundle.            #
################################################################################
erase() {
    rm -rf --preserve-root ${EXTRACT_BASE_DIR}
}

###############################################################################
# Writes out the tar file from the bundle, verifies it's integrity and then   #
# extracts the tarball. If extraction is successful, the .tar file is deleted.#
###############################################################################
extract() {
    BASE_DIR=$(dirname ${EXTRACT_BASE_DIR})
    [ ! -e ${BASE_DIR} ] && mkdir -p ${BASE_DIR}

    echo -n "Extracting contents ... "
    tail -n+$(get_archive_offset) $SELF | tar -C $BASE_DIR -xm --no-same-owner -f -
    if [ $? -ne 0 ]; then
        echo "FAILED."
        echo "ERROR: Unable to extract $SELF"
        exit 5
    fi

    # ensure that directories are readable
    find $EXTRACT_BASE_DIR -type d -exec chmod 755 {} \;
    find $EXTRACT_BASE_DIR -type f -exec chmod 644 {} \;
    if [ -n "${CHCON_BIN}" ];
    then
        ${CHCON_BIN} -R system_u:object_r:httpd_sys_content_t:s0 ${EXTRACT_BASE_DIR} >/dev/null 2>&1
    fi

    echo " done."
}

extract_sources() {
    if [[ ${SRC_PACKAGE_NAME} == 'undefined' ]]; then
        echo
        echo "ERROR: Sources are not packaged with this catalog bundle."
        echo
        exit 1
    fi

    echo -n "Extracting sources ... "
    tail -n+$(get_archive_offset) $SELF | tar -xm -f- ${BUNDLE_NAME}/${SRC_PACKAGE_NAME} -O > ${SRC_PACKAGE_NAME}
    if [ $? -ne 0 ]; then
        echo "FAILED."
        echo "ERROR: Unable to extract $SELF"
        exit 5
    fi
    echo "done."

}

print_feed_json() {
    [[ -z ${LOGO_EXTRACT_DIR} ]] && LOGO_EXTRACT_DIR="@@@@LOGOEXTRACTDIR@@@@"

    local LOGO_CHECKSUM='@@@@LOGOCHECKSUM@@@@'
    local LOGO_ENC_DATA="$(awk  -v TOTAL=1 '/^__ENTRY_LOGO__$/{CURR++;next} /^__ARCHIVE__$/{exit 0} (TOTAL==CURR){ print }' $0)"

    ## Spit out the feed data.
    echo -n "{\"_embedded\":{"
    echo -n "\"feed_version\" : 4,"
    echo -n     "\"entries\":[{"
    if [[ "${LOGO_ENC_DATA}" != 'undefined' ]];
    then
        ## The data is gziped and then encoded with base64.
        echo -n         "\"logo\": {\"encoded_data\": \"${LOGO_ENC_DATA}\","
        echo -n                    "\"checksum\":\"${LOGO_CHECKSUM}\"},"
    fi
    echo -n         "\"config_api_version\":@@@CONFIGAPIVER@@@,"
    echo -n         "\"catalog_api_version\":@@@CATALOGAPIVER@@@,"
    echo -n         "\"distro_id\":\"@@@DISTRO@@@\","
    echo -n         "\"label\":{\"name\":\"@@@NAME@@@\",\"description\":\"@@@DESCRIPTION@@@\"},"
    echo -n         "\"version\":\"@@@VERSION@@@\","
    echo -n         "\"independent\": @@@INDEPENDENT@@@,"
    echo -n         "\"osclass\": \"@@@IMAGEOSCLASS@@@\","
    echo -n         "\"osmajor\": \"@@@IMAGEOSMAJOR@@@\","
    echo -n         "\"image_name\": \"@@@IMAGE_NAME@@@\","
    if [[ "${REGISTRY_AUTH_ENABLED}" != 'undefined' ]];
    then
      echo -n        "\"registry_auth_enabled\": \"@@@REGISTRY_AUTH_ENABLED@@@\","
      echo -n        "\"content_trust_enabled\": \"@@@CONTENT_TRUST_ENABLED@@@\","
    fi
    echo -n         "\"built_on_docker\": \"@@@BUILTONDOCKER@@@\""
    echo -n     "}]}}"
}

#
# Returns a json object with paths to all the files installed by the bundle.
# NOTE: We try to handle the case where appconfig and image files are not
#       installed by this bundle but, in reality, the catalogsdk always
#       packages them for now.
print_file_json() {
    echo -n "{\"bundledir\":\"${EXTRACT_BASE_DIR}\","
    echo -n "\"entry\":\"${ENTRY_JSON_PATH}\""

    if [[ -n ${ENTRY_SETUP_PATH} ]];
    then
        echo -n ",\"appconfig\":\"${ENTRY_SETUP_PATH}\""
    fi

    if [[ -n ${ENTRY_IMAGE_PATH} ]];
    then
        echo -n ",\"image\":\"${ENTRY_IMAGE_PATH}\""
    fi
    echo -n "}"
}


print_help() {
    echo
    echo "BlueData Bundle usage: $0 [ options ]"
    echo
    echo "When no arguments are provided, the file is extracted and the installer"
    echo "is invoked automatically. Extracted files are stored (by default) at "
    echo "$EXTRACT_BASE_DIR/."
    echo ""
    echo " Available command line options:"
    echo "             -h/--help : Prints bundle usage details and exit."
    echo ""
    echo "                --meta : Display the metadata of the catalog entry."
    echo ""
    echo "              --verify : Verify bundle checksum and exit."
    echo "             --extract : Extract the payload. $(dirname ${EXTRACT_BASE_DIR}) is "
    echo "                         used as the default base directroy. It may be"
    echo "                         overriden by defining an environment variable"
    echo "                         EXTRACT_BASE_DIR to point to the desired base"
    echo "                         directory before invoking the bundle with this"
    echo "                         option."
    echo "     --extract-sources : Only extract the sources archive to from the"
    echo "                         catalog bundle. This will not extract any "
    echo "                         components from the bundle."
    echo

    if [ "$BUILD_TYPE" == 'debug' ]; then
        echo " BlueData internal options:"
        echo "        --feed : Prints the feed metadata for the catalog packaged"
        echo "                 in this bundle represented as JSON data."
        echo "       --files : Returns the location of all the files extracted."
        echo "                 The data is represented as JSON data"
        echo "     --payload : Writes the tgz payload and the decompress script"
        echo "                 for this bundle to respective files."
    fi
}

parse_options() {
    while [ $# -gt 0 ]; do
        case $1 in
            --erase)
                ERASE=true
                shift
                ;;
            --extract)
                EXTRACT_ONLY='true'
                shift
                ;;
            --extract-sources)
                EXTRACT_SOURCES='true'
                shift
                ;;
            --feed)
                FEED='true'
                shift
                ;;
            --files)
                FILES='true'
                shift
                ;;
            -h|--help)
                print_help
                exit 0
                ;;
            --meta)
                META='true'
                shift
                ;;
            --payload)
                PAYLOAD='true'
                shift
                ;;
            --verify)
                VERIFY_ONLY='true'
                shift
                ;;
            *)
                echo "ERROR: Unknown option: $1"
                exit 1
                ;;
        esac
    done
}

parse_options "$@"

if [ "${ERASE}" == 'true' ];
then
    erase
    exit $?
fi

if [ "$PAYLOAD" == 'true' ];
then
    sed -e "/^__ARCHIVE__$/q" $SELF > decompress.sh
    tail -n+$(get_archive_offset) $SELF > payload.tar
    exit $?
fi

if [ "${META}" == 'true' ];
then
    echo -e "${BOLD}Catalog Entry Metadata${END}"
    echo "                 Name : @@@NAME@@@ "
    echo "              Version : @@@VERSION@@@ "
    echo "             OS Class : @@@IMAGEOSCLASS@@@ "
    echo "             OS Major : @@@IMAGEOSMAJOR@@@ "
    echo "      Built On Docker : @@@BUILTONDOCKER@@@"
    echo "            Distro Id : @@@DISTRO@@@ "
    echo "   Config API Version : @@@CONFIGAPIVER@@@ "
    echo "  Catalog API Version : @@@CATALOGAPIVER@@@ "

    exit 0
fi

if [ "$VERIFY_ONLY" == 'true' ] && [ "$EXTRACT_ONLY" == 'true' ];
then
    verify
    extract
elif [ "$VERIFY_ONLY" == 'true' ];
then
    verify
elif [ "$EXTRACT_ONLY" == 'true' ];
then
    extract
elif [ "${EXTRACT_SOURCES}" == 'true' ];
then
    extract_sources
elif [ "${FEED}" == 'true' ];
then
    print_feed_json
elif [ "${FILES}" == 'true' ];
then
    print_file_json
else
    echo
    echo "ERROR: Directly executing this catalog bundle is an invalid operation."
    echo "       Please follow catalog bundle installation instructions from"
    echo "       BlueData EPIC's administration guide."
    echo
    exit 1
fi

exit 0

__ENTRY_LOGO__
@@@@LOGO_ENC_DATA@@@@
__ARCHIVE__
