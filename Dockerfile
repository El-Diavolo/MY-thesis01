FROM kalilinux/kali-rolling

COPY  . /home/kali/Desktop/MY-Thesis/

WORKDIR /home/kali/Desktop/MY-Thesis

RUN apt-get update -y

EXPOSE 80
EXPOSE 443
