FROM kalilinux/kali-rolling

COPY  . /usr/src/MY-Thesis/

WORKDIR /usr/src/MY-Thesis/

RUN apt-get update && \
    apt-get install -y git nmap ffuf sublist3r nuclei python3  && \
    apt-get clean 

RUN git clone https://github.com/projectdiscovery/httpx.git | cd httpx/cmd/httpx; go build | mv httpx /usr/local/bin/ | httpx -h

EXPOSE 80
EXPOSE 443
