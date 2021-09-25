FROM ubuntu:18.04

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y \
        g++ cmake build-essential autoconf automake subversion && \
    rm -rf /var/lib/apt/lists/*
RUN svn checkout http://voip.null.ro/svn/yate/trunk yate && \
    cd yate && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make install-noapi && \
    ldconfig && \
    cd .. && \
    rm -rf yate

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y curl ca-certificates && \
    curl -o /etc/apt/trusted.gpg.d/agp-debian-key.gpg http://download.ag-projects.com/agp-debian-key.gpg && \
    echo "deb     http://ag-projects.com/ubuntu bionic main">>/etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y python3 python-sipsimple sipclients && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY . .
RUN test/prepare.sh
CMD ["python3", "test/test.py"]
