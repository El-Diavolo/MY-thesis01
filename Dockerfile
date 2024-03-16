FROM kalilinux/kali-rolling

COPY  . /usr/src/MY-Thesis/

WORKDIR /usr/src/MY-Thesis/

RUN apt-get update && \
    apt-get install -y git nmap ffuf sublist3r nuclei shodan python3 subfinder httpx && \
    apt-get clean 


EXPOSE 80
EXPOSE 443