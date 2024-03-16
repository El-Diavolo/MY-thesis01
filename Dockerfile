FROM kalilinux/kali-rolling

COPY  c:/Users/hamoo/Desktop/thesis/MY-thesis01/Hamood Thesis/main.py /home/kali/Desktop/MY-Thesis/

WORKDIR /home/kali/Desktop/MY-Thesis

RUN apt-get update && apt-get upgrade

ARG USER=testuser
ARG PASS=3112

RUN useradd -m $USER -p $(openssl passwd $PASS) && \
    usermod -aG sudo $USER && \
    chsh -s /bin/bash $USER

EXPOSE 80
EXPOSE 443
