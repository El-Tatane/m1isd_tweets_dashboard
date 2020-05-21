# Pull base image.
FROM ubuntu:18.04

# Install
RUN \
  apt-get -y update  && \
  apt-get -y upgrade && \
  apt-get install -y python3-pip python3-dev locales

# Fix encoding
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Get dependencies
COPY ./ /app/

RUN ln -s /app/src/python/my_framework /usr/lib/python3/dist-packages/

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r /app/requirements.txt

# Define default command
#ENTRYPOINT [ "python3", "/app/src/python/main.py" ]
CMD tail -f /dev/null