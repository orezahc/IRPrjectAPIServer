FROM ubuntu:latest

EXPOSE 80
ENTRYPOINT ["/usr/bin/docker-entry"]
CMD ["--help"]

# Packages
RUN apt-get update
RUN apt-get install -y \
	git \
    libssl-dev \
    openssl \
    python3 \
    python3-pip

# PIP Upgrade
RUN pip3 install --upgrade pip

# Platform Setup
ADD app /usr/local/etc/app
RUN pip3 install -r /usr/local/etc/app/requirements.txt
ADD docker-entry /usr/bin/docker-entry
RUN chmod +x /usr/bin/docker-entry
