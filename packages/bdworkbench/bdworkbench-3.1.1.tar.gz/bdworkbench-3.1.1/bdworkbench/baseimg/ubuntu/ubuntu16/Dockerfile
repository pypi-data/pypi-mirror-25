FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y openssh-server sudo python python-setuptools net-tools  \
                       iproute2 erlang vim init-system-helpers bash-completion \
                       sssd sssd-ldap sssd-krb5 libpam-modules libpam-runtime  \
                       libpam-ldap libpam-krb5 libpam-sss libpam-passwdqc      \
                       libnss-ldapd libnss-sss python-sss python-ldap          \
                       ldap-utils libpython2.7-stdlib passwd libkrb5-3         \
                       krb5-user krb5-k5tls libsmbclient libsmbclient-dev      \
                       auth-client-config auditd libaudit-dev libaudit-common  \
                       language-pack-en iputils-ping

ADD deps/* /var/tmp/deps/
RUN cd /var/tmp/deps/elementtree-1.2-20040618; python setup.py install &&      \
    cd /var/tmp/deps/meld3-1.0.2; python setup.py install &&                   \
    cd /var/tmp/deps/supervisor-3.3.1; python setup.py install &&              \
    rm -rf /var/tmp/deps

## Generate a random password for root user for better security.
RUN passwd -l root

## Create a bluedata system user
RUN useradd -r -m -s /bin/bash bluedata; mkdir /home/bluedata/.ssh;            \
      chmod go-rx /home/bluedata/.ssh; chown -R bluedata:bluedata /home/bluedata
RUN echo 'Defaults:bluedata !requiretty\n\nbluedata ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/bluedata

## Don't require tty for any sudo commands.
RUN sed -i  's/Defaults    requiretty/#Defaults    requiretty/' /etc/sudoers

# RHEL is missing /sbin in the path. But, its okay to redefine for CentOS too.
ENV PATH $PATH:/sbin

## Limits configuration.
ADD ./limits-90-nproc.conf /etc/security/limits.d/90-nproc.conf

## Configuring SSH server.
RUN mkdir /var/run/sshd
RUN echo "y" | ssh-keygen -P '' -t rsa -f /etc/ssh/ssh_host_rsa_key
RUN echo "y" | ssh-keygen -P '' -t dsa -f /etc/ssh/ssh_host_dsa_key
RUN sed -i '/pam_loginuid.so/c session    optional     pam_loginuid.so'  /etc/pam.d/sshd
RUN sed -i '/^#PermitRootLogin yes$/d; $a PermitRootLogin no' /etc/ssh/sshd_config

RUN mkdir -p /etc/bluedata
ADD base_img_version /etc/bluedata/base_img_version
RUN chown -R bluedata:bluedata /etc/bluedata

## Configure supervisord
ADD supervisord.conf /etc/

## BlueData Management expects the supervisord to be at /usr/bin
RUN ln -sf /usr/local/bin/supervisord /usr/bin/supervisord

## Start default services (sshd, rsyslog etc.) at container bootup.
ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
