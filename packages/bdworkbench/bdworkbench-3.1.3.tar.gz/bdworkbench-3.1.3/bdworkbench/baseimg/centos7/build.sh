#!/bin/bash
#
# Builds CentOS/RHEL 6.x and 7.x images.
#set -x

RHEL7x='false'
CENTOS7x='false'

IMGVERSION=''
TEMPLATE_BASE=''

[[ -z "${RHEL7_UPSTREAM}" ]] && RHEL7_UPSTREAM="rhel7:latest"
[[ -z "${CENTOS7_UPSTREAM}" ]] && CENTOS7_UPSTREAM="centos:centos7"

print_help() {
    echo
    echo "USAGE: $0 [ -h ]"
    echo
    echo "                  -h    : Prints usage details and exits."
    echo "                --rhel7 : Build a RHEL 7.x image."
    echo "              --centos7 : Build a CentOS 7.x image."
    echo
    echo "           --imgversion : Base image version of MAJOR.MINOR format."
    echo "           --imgorgname : Organization name of the base image builder."
    echo "--epic-base-img-version : Version indicating which EPIC features are supported."
    echo ""
    echo "         --template_dir : Template base directory."
    echo
}

parse_options() {
    while [ $# -gt 0 ]; do
        case $1 in
            -h|--help)
                print_help
                exit 0
                ;;
            --centos7)
                CENTOS7x='true'
                shift
                ;;
            --epic-base-version)
                EPIC_BASE_IMG_VERSION=$2;
                shift 2
                ;;
            --imgorgname)
                ORGNAME=$2
                shift 2
                ;;
            --rhel7)
                RHEL7x='true'
                shift
                ;;
            --template_dir)
                TEMPLATE_BASE=$2
                shift 2
                ;;
            --imgversion)
                IMGVERSION=$2
                shift 2
                ;;
            --)
                shift
                ;;
            *)
                echo "Unknown option $1."
                print_help
                exit 1
                ;;
        esac
    done

    if [[ -z "${IMGVERSION}" ]] || [[ -z "${TEMPLATE_BASE}" ]];
    then
        echo "ERROR: --imgversion and --template_dir must be specified."
        exit 1
    fi

    if [[ -z "${ORGNAME}" ]] || [[ -z "${IMGVERSION}" ]];
    then
        echo "ERROR: --imgorgname and --imgversion are mandatory."
        exit 1
    fi

    [[ -z ${EPIC_BASE_IMG_VERSION} ]] && EPIC_BASE_IMG_VERSION=${IMGVERSION}
}

SHORTOPTS="h"
LONGOPTS="centos7,rhel7,imgorgname:,imgversion:,epic-base-version:,template_dir:,help"
OPTS=$(getopt -u --options=$SHORTOPTS --longoptions=$LONGOPTS -- "$@")
if [ $? -ne 0 ]; then
    echo "ERROR: Unable to parse the option(s) provided."
    print_help
    exit 1
fi

parse_options $OPTS

RHEL_SUBSCRIPTION="RUN subscription-manager register --username=${RHEL_USERNAME} --password=${RHEL_PASSWORD};subscription-manager attach --auto;subscription-manager repos --disable *eus*"
IMAGE_RHEL_FOOTER="subscription-manager unsubscribe --all;subscription-manager unregister;subscription-manager clean"

build_docker_image() {
    docker build -t $1 $2
    if [[ $? -ne 0 ]]; then
        echo "ERROR: Failed to build docker image: $1"
        exit 1
    fi
}

create_docker_tag() {
    docker tag $1 $2
    if [[ $? -ne 0 ]]; then
        echo "ERROR: Failed to tag docker image: $1"
        exit 1
    fi
}

echo "${EPIC_BASE_IMG_VERSION}" > ${TEMPLATE_BASE}/base_img_version

if [[ "${CENTOS7x}" == 'true' ]];
then
    echo "Build CentOS 7.x base image"

    cp ${TEMPLATE_BASE}/Dockerfile.template  ${TEMPLATE_BASE}/Dockerfile
    sed -i "s~@@@@BASE_IMAGE_HEADER@@@@~FROM ${CENTOS7_UPSTREAM}\n\nRUN ~g" ${TEMPLATE_BASE}/Dockerfile
    sed -i "/.*@@@@BASE_IMAGE_FOOTER@@@@.*$/d" ${TEMPLATE_BASE}/Dockerfile

    build_docker_image "${ORGNAME}/centos7:${IMGVERSION}" ${TEMPLATE_BASE}
    create_docker_tag "${ORGNAME}/centos7:${IMGVERSION}" "${ORGNAME}/centos7:latest"
fi

if [[ "${RHEL7x}" == 'true' ]];
then
    echo "Build RHEL 7.x base image"

    if [[ -n "${RHEL_USERNAME}" ]];
    then
        BASEIMG_RHEL7_HEADER="FROM ${RHEL7_UPSTREAM}\n\n${RHEL_SUBSCRIPTION}; "
        BASEIMG_RHEL7_FOOTER=${IMAGE_RHEL_FOOTER}
    else
        # If we are building on an RHEL7 base, then the container does not need
        # subsctiption.
        BASEIMG_RHEL7_HEADER="FROM ${RHEL7_UPSTREAM}\n\nRUN "
        BASEIMG_RHEL7_FOOTER=""

        sed -i "/.*@@@@BASE_IMAGE_FOOTER@@@@.*$/d" ${TEMPLATE_BASE}/Dockerfile
    fi

    cp ${TEMPLATE_BASE}/Dockerfile.template  ${TEMPLATE_BASE}/Dockerfile
    sed -i "s~@@@@BASE_IMAGE_HEADER@@@@~${BASEIMG_RHEL7_HEADER}~g" ${TEMPLATE_BASE}/Dockerfile
    sed -i "s~@@@@BASE_IMAGE_FOOTER@@@@~${BASEIMG_RHEL7_FOOTER}~g" ${TEMPLATE_BASE}/Dockerfile

    build_docker_image "${ORGNAME}/rhel7:${IMGVERSION}" ${TEMPLATE_BASE}
    create_docker_tag "${ORGNAME}/rhel7:${IMGVERSION}" "${ORGNAME}/rhel7:latest"
fi
