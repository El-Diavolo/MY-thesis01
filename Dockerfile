FROM kalilinux/kali-rolling

ENV HOST_IP=host.docker.internal

# Copy your application source
COPY . /usr/src/MY-Thesis/
WORKDIR /usr/src/MY-Thesis/

# Install tools
RUN apt-get update && \
    apt-get install -y git gobuster nmap ffuf sublist3r nuclei python3 seclists nano python3-pip && \
    pip3 install python-nmap xmltodict shodan httpx asyncio python-Wappalyzer && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install EyeWitness
RUN git clone https://github.com/RedSiege/EyeWitness.git /opt/EyeWitness && \
    chmod +x /opt/EyeWitness/Python/setup/setup.sh && \
    /opt/EyeWitness/Python/setup/setup.sh

# Install wappalyzer-cli
RUN git clone https://github.com/gokulapap/wappalyzer-cli /opt/wappalyzer-cli && \
    pip3 install -e /opt/wappalyzer-cli

EXPOSE 80
EXPOSE 443
