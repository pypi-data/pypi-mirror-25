# Copyright (c) 2016 BlueData Software, Inc.
#

UBUNTU_BASE  := $(shell pwd)

EPIC_BASE_IMG_VERSION ?= 3.0
BASE_IMG_ORGNAME      ?= bluedata
BASE_IMG_VERSION      ?= $(EPIC_BASE_IMG_VERSION)


DEPS         := $(addprefix $(UBUNTU_BASE)/ubuntu16/,Dockerfile supervisord.conf limits-90-nproc.conf)

.PHONY: all clean distclean ubuntu16

all: ubuntu16

ubuntu16: $(DEPS)
	$(V)set -ex;                                                                \
echo $(EPIC_BASE_IMG_VERSION) > $(UBUNTU_BASE)/$@/base_img_version;         \
docker build -t $(BASE_IMG_ORGNAME)/$@:$(BASE_IMG_VERSION) $(UBUNTU_BASE)/$@;     \
docker tag $(BASE_IMG_ORGNAME)/$@:$(BASE_IMG_VERSION) $(BASE_IMG_ORGNAME)/$@:latest

clean:
	$(V)rm -f $(UBUNTU_BASE)/*/base_img_version

distclean: clean
	$(V)docker rmi -f $(BASE_IMG_ORGNAME)/ubuntu16:$(BASE_IMG_VERSION) $(BASE_IMG_ORGNAME)/ubuntu16:latest
