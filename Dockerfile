FROM kalilinux/kali-rolling

COPY  . /home/kali/Desktop/MY-Thesis/

WORKDIR /home/kali/Desktop/MY-Thesis

RUN apt-get update -y && apt-get install -y 

ARG USER=testuser
ARG PASS=1234

RUN useradd -m $USER -p $(openssl passwd $PASS) && \
    usermod -aG sudo $USER && \
    chsh -s /bin/bash $USER

EXPOSE 80
EXPOSE 443
