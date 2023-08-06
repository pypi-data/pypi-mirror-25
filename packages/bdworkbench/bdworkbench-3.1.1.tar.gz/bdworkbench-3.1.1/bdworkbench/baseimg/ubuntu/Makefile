# Copyright (c) 2016 BlueData Software, Inc.
#

UBUNTU_BASE  := $(shell pwd)

CATALOG_BASE_IMG_VERSION ?= 3.0

DEPS         := $(addprefix $(UBUNTU_BASE)/ubuntu16/,Dockerfile supervisord.conf limits-90-nproc.conf)

.PHONY: all clean distclean ubuntu16

all: ubuntu16

ubuntu16: $(DEPS)
	$(V)set -ex;                                                                \
echo $(CATALOG_BASE_IMG_VERSION) > $(UBUNTU_BASE)/$@/base_img_version;         \
docker build -t bluedata/$@:$(CATALOG_BASE_IMG_VERSION) $(UBUNTU_BASE)/$@;     \
docker tag bluedata/$@:$(CATALOG_BASE_IMG_VERSION) bluedata/$@:latest

clean:
	$(V)rm -f $(UBUNTU_BASE)/*/base_img_version

distclean: clean
	$(V)docker rmi -f bluedata/ubuntu16:$(CATALOG_BASE_IMG_VERSION) bluedata/ubuntu16:latest
