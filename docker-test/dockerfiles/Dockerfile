FROM debian:10.3 AS builder
WORKDIR /build/
RUN echo "deb-src http://deb.debian.org/debian bullseye main" >> \
    /etc/apt/sources.list && \
    apt-get update && apt-get -y install dpkg-dev && \
    apt-get source python3-yaml && \
    apt-get -y build-dep python3-yaml && \
    cd -- $(find . -type d -name pyyaml-\* -exec basename {} \;) && \
    apt-get clean && \
    DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage -rfakeroot -uc -b

FROM debian:10.3
ENV LANG en_US.UTF8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
COPY --from=builder /build/python3-yaml_*.deb /tmp/
RUN apt-get update && \
    apt-get -y install locales-all locales python3 \
    python3-pyqt5 python3-pyqtgraph python3-numpy python3-serial \
    python3-yaml python3-pytest python3-pytestqt python3-coverage \
    python3-pytest-xvfb python3-xvfbwrapper \
    minicom vim virtualenv libatlas3-base exfat-utils qt5-default \
    pyqt5-dev pyqt5-dev-tools exfat-fuse esptool && \
    apt-get clean && \
    dpkg -i /tmp/python3-yaml_*.deb && \
    groupadd -g 1000 pi && useradd -u 1000 -g 1000 -G dialout -m \
      -s /bin/bash pi && \
    ln -s /usr/bin/pytest-3 /usr/bin/pytest && \
    ln -s /usr/bin/python3 /usr/bin/python
USER pi

