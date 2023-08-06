#!/bin/bash
#
# Builds CentOS/RHEL 6.x and 7.x images.
#set -x

RHEL6x='false'
RHEL7x='false'
CENTOS6x='false'
CENTOS7x='false'

IMGVERSION=''
TEMPLATE_BASE=''

print_help() {
    echo
    echo "USAGE: $0 [ -h ]"
    echo
    echo "            -h    : Prints usage details and exits."
    echo "          --rhel7 : Build only a RHEL 7.x image."
    echo "        --centos7 : Build only a CentOS 7.x image."
    echo
    echo "     --imgversion : Base image version of MAJOR.MINOR format."
    echo "   --template_dir : Template base directory."
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
            --centos7)
                CENTOS7x='true'
                shift
                ;;
            --rhel6)
                RHEL6x='true'
                shift
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

    if [[ -z "${IMGVERSION}" ]] || [[ -z "${TEMPLATE_BASE}" ]]; then
        echo "ERROR: --imgversion and --template_dir must be specified."
        exit 1
    fi

    if [[ "${RHEL6x}" == 'true' || ${RHEL7x} == 'true' ]];
    then
        if [[ -z ${RHEL_USERNAME} || -z ${RHEL_PASSWORD} ]];
        then
            echo "ERROR: RHEL username/password no specified."
            echo "Please set RHEL_USERNAME and RHEL_PASSWORD env variables."
            exit 2
        fi
    fi
}

SHORTOPTS="h"
LONGOPTS="centos7,rhel7,imgversion:,template_dir:,help"
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

echo "${IMGVERSION}" > ${TEMPLATE_BASE}/base_img_version

if [[ "${CENTOS7x}" == 'true' ]];
then
    echo "Build CentOS 7.x base image"

    cp ${TEMPLATE_BASE}/Dockerfile.template  ${TEMPLATE_BASE}/Dockerfile
    sed -i "s~@@@@BASE_IMAGE_HEADER@@@@~FROM centos:centos7\n\nRUN ~g" ${TEMPLATE_BASE}/Dockerfile
    sed -i "/.*@@@@BASE_IMAGE_FOOTER@@@@.*$/d" ${TEMPLATE_BASE}/Dockerfile

    build_docker_image "bluedata/centos7:${IMGVERSION}" ${TEMPLATE_BASE}
    create_docker_tag "bluedata/centos7:${IMGVERSION}" "bluedata/centos7:latest"
fi

if [[ "${RHEL7x}" == 'true' ]];
then
    echo "Build RHEL 7.x base image"

    BASEIMG_RHEL7_HEADER="FROM rhel7:latest\n\n${RHEL_SUBSCRIPTION}"

    cp ${TEMPLATE_BASE}/Dockerfile.template  ${TEMPLATE_BASE}/Dockerfile
    sed -i "s~@@@@BASE_IMAGE_HEADER@@@@~${BASEIMG_RHEL7_HEADER};~g" ${TEMPLATE_BASE}/Dockerfile
    sed -i "s~@@@@BASE_IMAGE_FOOTER@@@@~${IMAGE_RHEL_FOOTER}~g" ${TEMPLATE_BASE}/Dockerfile

    build_docker_image "bluedata/rhel7:${IMGVERSION}" ${TEMPLATE_BASE}
    create_docker_tag "bluedata/rhel7:${IMGVERSION}" "bluedata/rhel7:latest"
fi
