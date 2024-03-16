FROM kalilinux/kali-rolling

COPY  . /home/kali/Desktop/MY-Thesis/

WORKDIR /home/kali/Desktop/MY-Thesis

RUN apt-get update && apt-get upgrade -y

ARG USER=testuser
ARG PASS=3112

RUN useradd -m $USER -p $(openssl passwd $PASS) && \
    usermod -aG sudo $USER && \
    chsh -s /bin/bash $USER

EXPOSE 80
EXPOSE 443
