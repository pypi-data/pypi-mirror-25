# Copyright (c) 2016 BlueData Software, Inc.
#

CENTOS_BASE   := $(shell pwd)

TEMPLATE_BASE := $(CENTOS_BASE)/template
CENTOS_BUIDLER:= $(CENTOS_BASE)/build.sh

EPIC_BASE_IMG_VERSION ?= 2.1
BASE_IMG_ORGNAME      ?= bluedata
BASE_IMG_VERSION      ?= $(EPIC_BASE_IMG_VERSION)

DEPS         := $(addprefix $(TEMPLATE_BASE)/,Dockerfile.template supervisord.conf limits-90-nproc.conf)

.PHONY: all clean distclean centos6 rhel6

all: centos6 rhel6

centos6: $(DEPS)
	$(V)bash $(CENTOS_BUIDLER) --epic-base-version $(EPIC_BASE_IMG_VERSION)    \
                               --imgorgname $(BASE_IMG_ORGNAME)                \
                               --imgversion $(BASE_IMG_VERSION)                \
                               --template_dir $(TEMPLATE_BASE) --centos6

rhel6: $(DEPS)
	$(V)bash $(CENTOS_BUIDLER) --epic-base-version $(EPIC_BASE_IMG_VERSION)    \
                               --imgorgname $(BASE_IMG_ORGNAME)                \
                               --imgversion $(BASE_IMG_VERSION)                \
                               --template_dir $(TEMPLATE_BASE) --rhel6

clean:
	$(V) rm -f $(CENTOS_BASE)/template/base_img_version  $(CENTOS_BASE)/*/Dockerfile

distclean: clean
	$(V)docker rmi -f $(BASE_IMG_ORGNAME)/centos6:latest $(BASE_IMG_ORGNAME)/rhel6:latest
	$(V)docker rmi -f $(BASE_IMG_ORGNAME)/centos6:$(BASE_IMG_VERSION) $(BASE_IMG_ORGNAME)/rhel6:$(BASE_IMG_VERSION)
