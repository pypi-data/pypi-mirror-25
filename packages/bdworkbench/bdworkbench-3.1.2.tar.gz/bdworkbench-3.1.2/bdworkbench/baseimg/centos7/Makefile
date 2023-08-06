# Copyright (c) 2016 BlueData Software, Inc.
#

CENTOS_BASE   := $(shell pwd)

TEMPLATE_BASE := $(CENTOS_BASE)/template
CENTOS_BUIDLER:= $(CENTOS_BASE)/build.sh

EPIC_BASE_IMG_VERSION ?= 3.0
BASE_IMG_ORGNAME      ?= bluedata
BASE_IMG_VERSION      ?= $(EPIC_BASE_IMG_VERSION)

DEPS         := $(addprefix $(TEMPLATE_BASE)/,Dockerfile.template limits-90-nproc.conf)

.PHONY: all clean distclean centos7 rhel7

all: centos7 rhel7

centos7: $(DEPS)
	$(V)bash $(CENTOS_BUIDLER) --epic-base-version $(EPIC_BASE_IMG_VERSION)    \
                               --imgorgname $(BASE_IMG_ORGNAME)                \
                               --imgversion $(BASE_IMG_VERSION)                \
                               --template_dir $(TEMPLATE_BASE) --centos7

rhel7: $(DEPS)
	$(V)bash $(CENTOS_BUIDLER) --epic-base-version $(EPIC_BASE_IMG_VERSION)    \
                               --imgorgname $(BASE_IMG_ORGNAME)                \
                               --imgversion $(BASE_IMG_VERSION)                \
                               --template_dir $(TEMPLATE_BASE) --rhel7

clean:
	$(V) rm -f $(CENTOS_BASE)/template/base_img_version  $(CENTOS_BASE)/*/Dockerfile

distclean: clean
	$(V)docker rmi -f $(BASE_IMG_ORGNAME)/centos7:latest $(BASE_IMG_ORGNAME)/rhel7:latest
	$(V)docker rmi -f $(BASE_IMG_ORGNAME)/centos7:$(BASE_IMG_VERSION) $(BASE_IMG_ORGNAME)/rhel7:$(BASE_IMG_VERSION)
