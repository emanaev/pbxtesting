FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y curl ca-certificates
RUN curl -o /etc/apt/trusted.gpg.d/agp-debian-key.gpg http://download.ag-projects.com/agp-debian-key.gpg
RUN echo "deb     http://ag-projects.com/ubuntu bionic main">>/etc/apt/sources.list 
RUN apt-get update
RUN apt-get install -y python-sipsimple sipclients
WORKDIR /root
COPY sipsimple.sh /
