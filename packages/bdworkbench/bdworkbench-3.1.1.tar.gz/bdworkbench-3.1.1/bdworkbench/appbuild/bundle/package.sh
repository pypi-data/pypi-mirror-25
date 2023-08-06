#!/usr/bin/env bash
################################################################################
#
#
#
#
######
set -e
[[ -n "${DEBUG}" && "${DEBUG}" == 'true' ]] && set -x

OSNAME=$(uname -s)
OS_LINUX='Linux'
OS_DARWIN='Darwin'

if [[ "${OSNAME}" != "${OS_LINUX}" && "${OSNAME}" != "${OS_DARWIN}" ]];
then
    echo "ERROR: Unsupported os: ${OS}."
    exit 1
fi

BUNDLE_DIR=$(dirname ${BASH_SOURCE[0]})

VERBOSE='false'
BUILD_TYPE='release'

DECOMPRESS_FILE=${BUNDLE_DIR}/decompress.sh
LOGO_EXTRACT_DIR='/opt/bluedata/catalog/bundle/logos'
CATALOG_EXTRACT_DIR='/opt/bluedata/catalog/bundle/install'

print_help() {
    echo "$0 [ OPTIONS ]"
    echo
    echo "Available options:"
    echo "       -c/--config : A package configuration file with all the"
    echo "                     parameters required for packaging the catalog."
    echo "         -h/--help : Show this help message and exit. "
    echo "      -v/--verbose : Show verbose logs when packaging."
    echo
}

parse_opts() {
    while [ $# -gt 0 ]; do
        case $1 in
            -c|--config)
                CONFIG_FILE=$2
                shift 2
                ;;
            -h|--help)
                print_help
                exit 0
                ;;
            -v|--verbose)
                VERBOSE='true'
                shift
                ;;
            --)
                shift
                ;;
            *)
                echo "Unknown argument $1"
                exit 2
                ;;
        esac
    done

    if [[ -z "${CONFIG_FILE}" ]]; then
        echo  "ERROR: -c/--config is a mandatory argument."
        exit 2
    fi

    if [[ ! -e "${CONFIG_FILE}" ]]; then
        echo "ERROR: File '${CONFIG_FILE}' does not exist."
        exit 2
    fi
}

SHORTOPTS="c:hv"
LONGOPTS="config:,help,verbose"
OPTS=$(getopt -u --options $SHORTOPTS --longoptions $LONGOPTS -- "$@")
if [[ $? -ne 0 ]]; then
    print_help

    exit 1
fi

parse_opts ${OPTS}

source ${CONFIG_FILE}

#### FIXME! ADD VALIDATION CODE ####

isUrlOrUndef() {
    local ARG=$1
    [[ "${ARG}" == 'undefined' ]] && return 0
    [[ "${ARG}" = 'http://'* ]] && return 0
    [[ "${ARG}" = 'https://'* ]] && return 0
    return 1
}

checksum() {
    local FILE=$1

    if [[ "${OSNAME}" == 'Linux' ]]; then
        echo $(md5sum ${FILE} | awk '{print $1}')
    elif [[ "${OSNAME}" == 'Darwin' ]]; then
        echo $(md5 ${FILE} | awk '{print $NF}')
    fi
}

log_verbose() {
    if [[ ${VERBOSE} == 'true' ]]; then
        echo "$@"
    fi
}


log_verbose "Creating/verifying build directories."
SANITIZED_DISTRO="$(echo ${DISTRO} | sed s:/:-:g)"
CATALOG_STAGING_DIR="${STAGING_DIR}/${SANITIZED_DISTRO}"
[[ -e "${CATALOG_STAGING_DIR}" ]] && rm -rf ${CATALOG_STAGING_DIR}
[[ ! -e "${CATALOG_STAGING_DIR}" ]] && mkdir -p ${CATALOG_STAGING_DIR}

CATALOG_NAME=bdcatalog-${IMAGEOSCLASS}-${SANITIZED_DISTRO}-${VERSION}

CATALOG_BASE_DIR=${CATALOG_STAGING_DIR}/${CATALOG_NAME}
mkdir -p ${CATALOG_BASE_DIR} && chmod 755 ${CATALOG_BASE_DIR}

log_verbose -n "Populating contents of the bundle's archive ... "
ENTRY_FILENAME="$(basename ${ENTRY})"
cp -f ${ENTRY} ${CATALOG_BASE_DIR}/${ENTRY_FILENAME}

if ! $(isUrlOrUndef ${IMAGE}); then
    DEST_IMAGE_DIR="${CATALOG_BASE_DIR}/${IMAGE_DIR}"
    mkdir -p ${DEST_IMAGE_DIR} && chmod 755 ${DEST_IMAGE_DIR}

    IMAGE_FILENAME="$(basename ${IMAGE})"
    cp -f ${IMAGE} ${DEST_IMAGE_DIR}/${IMAGE_FILENAME} && chmod 644 ${DEST_IMAGE_DIR}/${IMAGE_FILENAME}
else
    IMAGE_FILENAME='undefined'
fi

if ! $(isUrlOrUndef ${APPCONFIG_DIR}); then
    DEST_APPCONFIG_DIR="${CATALOG_BASE_DIR}/${APPCONFIG_DIR}"
    mkdir -p ${DEST_APPCONFIG_DIR} && chmod 755 ${DEST_APPCONFIG_DIR}

    APPCONFIG_FILENAME="$(basename ${APPCONFIG})"
    cp -f ${APPCONFIG} ${DEST_APPCONFIG_DIR}/${APPCONFIG_FILENAME} && \
    chmod 644 ${DEST_APPCONFIG_DIR}/${APPCONFIG_FILENAME}
else
    APPCONFIG_FILENAME="undefined"
fi
log_verbose "done."

if [[ -n "${SOURCES}" ]]; then
    log_verbose -n "Packaging sources into the bundle ... "

    SRC_DIR_NAME=${CATALOG_NAME}-src
    SRC_TARFILE=${SRC_DIR_NAME}.tgz

    SRC_BASE_DIR=${STAGING_DIR}/${SRC_DIR_NAME}
    SRC_TGT_TARFILE=${CATALOG_BASE_DIR}/${SRC_TARFILE}

    [[ -e ${STAGING_DIR} ]] && rm --preserve -rf ${SRC_BASE_DIR}/
    mkdir -p ${SRC_BASE_DIR}
    cp -rf $(echo ${SOURCES} | tr ';' ' ') ${SRC_BASE_DIR}
    chmod -R 755 ${SRC_BASE_DIR}

    tar cz -C ${STAGING_DIR} -f ${SRC_TGT_TARFILE} ${SRC_DIR_NAME}
    chmod 644 ${SRC_TGT_TARFILE}
    log_verbose "done."
else
    SRC_TARFILE='undefined'
fi

log_verbose -n "Creating bundle's archive ... "
TAR_FILE=${STAGING_DIR}/${CATALOG_NAME}.tar
tar -C ${CATALOG_STAGING_DIR} -cf ${TAR_FILE} ${CATALOG_NAME}
TAR_MD5SUM=$(checksum ${TAR_FILE})
log_verbose " done."

# Generate compressed and encoded Logo data
if ! $(isUrlOrUndef ${LOGO});
then
    if [[ "${OSNAME}" == "${OS_LINUX}" ]]; then
        LOGO_ENC_DATA="$(gzip -c ${LOGO} | base64 -w0)"
    elif [[ "${OSNAME}" == "${OS_DARWIN}" ]]; then
        LOGO_ENC_DATA="$(gzip -c ${LOGO} | base64)"
    fi
else
    LOGO_ENC_DATA="undefined"
fi
DEST_DECOMP=${STAGING_DIR}/decompress-${IMAGEOSCLASS}-${SANITIZED_DISTRO}.sh
cp -f ${DECOMPRESS_FILE} ${DEST_DECOMP}

sed -i "s|@@@@BUILDTYPE@@@@|${BUILD_TYPE}|" ${DEST_DECOMP}
sed -i "s|@@@@BUNDLENAME@@@@|${CATALOG_NAME}|" ${DEST_DECOMP}
sed -i "s|@@@@TAREXTRACTDIR@@@@|${CATALOG_EXTRACT_DIR}|g" ${DEST_DECOMP}
sed -i "s|@@@@TARENTRYJSON@@@@|${ENTRY_FILENAME}|" ${DEST_DECOMP}
sed -i "s|@@@@TARENTRYIMAGE@@@@|${IMAGE_FILENAME}|" ${DEST_DECOMP}
sed -i "s|@@@@TARENTRYSETUP@@@@|${APPCONFIG_FILENAME}|" ${DEST_DECOMP}
sed -i "s|@@@@TARFILECHECKSUM@@@@|${TAR_MD5SUM}|" ${DEST_DECOMP}

sed -i "s|@@@@LOGOEXTRACTDIR@@@@|${LOGO_EXTRACT_DIR}|" ${DEST_DECOMP}
sed -i "s|@@@@LOGOCHECKSUM@@@@|${LOGO_CHECKSUM}|" ${DEST_DECOMP}
sed -i "s|@@@@LOGO_ENC_DATA@@@@|${LOGO_ENC_DATA}|" ${DEST_DECOMP}

## Populate the catalog entry details for the self feed.
sed -i "s|@@@NAME@@@|${NAME}|g" ${DEST_DECOMP}
sed -i "s|@@@DISTRO@@@|${DISTRO}|g" ${DEST_DECOMP} ## Not the sanitized version.
sed -i "s|@@@IMAGEOSCLASS@@@|${IMAGEOSCLASS}|g" ${DEST_DECOMP}
sed -i "s|@@@IMAGEOSMAJOR@@@|${IMAGEOSMAJOR}|g" ${DEST_DECOMP}
sed -i "s|@@@BUILTONDOCKER@@@|${BUILTONDOCKER}|g" ${DEST_DECOMP}
sed -i "s|@@@IMAGE_NAME@@@|${IMAGE_NAME}|g" ${DEST_DECOMP}
sed -i "s|@@@REGISTRY_AUTH_ENABLED@@@|${REGISTRY_AUTH_ENABLED}|g" ${DEST_DECOMP}
sed -i "s|@@@CONTENT_TRUST_ENABLED@@@|${CONTENT_TRUST_ENABLED}|g" ${DEST_DECOMP}
sed -i "s|@@@VERSION@@@|${VERSION}|g" ${DEST_DECOMP}
sed -i "s|@@@DESCRIPTION@@@|${DESCRIPTION}|g" ${DEST_DECOMP}
sed -i "s|@@@INDEPENDENT@@@|${INDEPENDENT}|g" ${DEST_DECOMP}
sed -i "s|@@@CONFIGAPIVER@@@|${CONFIG_API_VERSION}|g" ${DEST_DECOMP}
sed -i "s|@@@CATALOGAPIVER@@@|${CATALOG_API_VERSION}|g" ${DEST_DECOMP}
sed -i "s|@@@SOURCEPACKAGE@@@|${SRC_TARFILE}|g" ${DEST_DECOMP}

[[ ! -e ${DELIVERABLE_DIR} ]] && mkdir -p ${DELIVERABLE_DIR}

log_verbose -n "Generating the catalog bundle ... "
CATALOG_BUNDLE="${DELIVERABLE_DIR}/${CATALOG_NAME}.bin"
cat ${DEST_DECOMP} ${TAR_FILE} > ${CATALOG_BUNDLE}
chmod +x ${CATALOG_BUNDLE}
log_verbose "done."
echo "Catalog bundle is saved at ${CATALOG_BUNDLE}"
