#!/bin/bash
#
# Builds CentOS/RHEL 6.x images.
#set -x

RHEL6x='false'
CENTOS6x='false'

IMGVERSION=''
TEMPLATE_BASE=''

[[ -z "${RHEL6_UPSTREAM}" ]] && RHEL6_UPSTREAM="rhel6:latest"
[[ -z "${CENTOS6_UPSTREAM}" ]] && CENTOS6_UPSTREAM="centos:centos6"

print_help() {
    echo
    echo "USAGE: $0 [ -h ]"
    echo
    echo "                  -h    : Prints usage details and exits."
    echo "                --rhel6 : Build a RHEL 6.x image."
    echo "              --centos6 : Build a CentOS 6.x image."
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
            --centos6)
                CENTOS6x='true'
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
            --rhel6)
                RHEL6x='true'
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

    if [[ -z "${IMGVERSION}" ]] || [[ -z "${TEMPLATE_BASE}" ]]; then
        echo "ERROR: --imgversion and --template_dir must be specified."
        exit 1
    fi

    if [[ "${RHEL6x}" == 'true' ]];
    then
        if [[ -z ${RHEL_USERNAME} || -z ${RHEL_PASSWORD} ]];
        then
            echo "ERROR: RHEL username/password not specified."
            echo "Please set RHEL_USERNAME and RHEL_PASSWORD env variables."
            exit 2
        fi
    fi

    [[ -z ${EPIC_BASE_IMG_VERSION} ]] && EPIC_BASE_IMG_VERSION=${IMGVERSION}
}

SHORTOPTS="h"
LONGOPTS="centos6,rhel6,imgorgname:,imgversion:,epic-base-version:,template_dir:,help"
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

if [[ "${CENTOS6x}" == 'true' ]];
then
    echo "Build CentOS 6.x base image"

    cp ${TEMPLATE_BASE}/Dockerfile.template  ${TEMPLATE_BASE}/Dockerfile
    sed -i "s~@@@@BASE_IMAGE_HEADER@@@@~FROM ${CENTOS6_UPSTREAM}\n\nRUN ~g" ${TEMPLATE_BASE}/Dockerfile
    sed -i "/.*@@@@BASE_IMAGE_FOOTER@@@@.*$/d" ${TEMPLATE_BASE}/Dockerfile

    build_docker_image "${ORGNAME}/centos6:${IMGVERSION}" ${TEMPLATE_BASE}
    create_docker_tag "${ORGNAME}/centos6:${IMGVERSION}" "${ORGNAME}/centos6:latest"
fi

if [[ "${RHEL6x}" == 'true' ]];
then
    echo "Build RHEL 6.x base image"

    cp ${TEMPLATE_BASE}/Dockerfile.template  ${TEMPLATE_BASE}/Dockerfile
    sed -i "s~@@@@BASE_IMAGE_HEADER@@@@~FROM ${RHEL6_UPSTREAM}\n\n${RHEL_SUBSCRIPTION};~g" ${TEMPLATE_BASE}/Dockerfile
    sed -i "s~@@@@BASE_IMAGE_FOOTER@@@@~${IMAGE_RHEL_FOOTER}~g" ${TEMPLATE_BASE}/Dockerfile

    build_docker_image "${ORGNAME}/rhel6:${IMGVERSION}" ${TEMPLATE_BASE}
    create_docker_tag "${ORGNAME}/rhel6:${IMGVERSION}" "${ORGNAME}/rhel6:latest"
fi
