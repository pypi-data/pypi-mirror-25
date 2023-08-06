# Copyright (c) 2016 BlueData Software, Inc.
#

CENTOS_BASE   := $(shell pwd)

TEMPLATE_BASE := $(CENTOS_BASE)/template
CENTOS_BUIDLER:= $(CENTOS_BASE)/build.sh

CATALOG_BASE_IMG_VERSION ?= 4.0

DEPS         := $(addprefix $(TEMPLATE_BASE)/,Dockerfile.template limits-90-nproc.conf)

.PHONY: all clean distclean centos7 rhel7

all: centos7 rhel7

centos7: $(DEPS)
	$(V)bash $(CENTOS_BUIDLER) --imgversion $(CATALOG_BASE_IMG_VERSION)        \
                          --template_dir $(TEMPLATE_BASE) --centos7

rhel7: $(DEPS)
	$(V)bash $(CENTOS_BUIDLER) --imgversion $(CATALOG_BASE_IMG_VERSION)        \
                          --template_dir $(TEMPLATE_BASE) --rhel7

clean:
	$(V) rm -f $(CENTOS_BASE)/template/base_img_version  $(CENTOS_BASE)/*/Dockerfile

distclean: clean
	$(V)docker rmi -f bluedata/centos7:latest  bluedata/rhel7:latest
