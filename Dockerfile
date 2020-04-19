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
COPY requirements.txt /tmp/
#COPY ./ /app

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r /tmp/requirements.txt


######## USEFUL DEV #####
RUN apt-get update && apt-get install -y openssh-server
#COPY ignore/dev_var_env_to_load.env /root/.ssh/environment
RUN mkdir /var/run/sshd
RUN echo 'root:azerty' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
#RUN sed -i 's/#PermitUserEnvironment no/PermitUserEnvironment yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
##### end usefull dev #######

# WORKDIR /app

# Define default command
#ENTRYPOINT [ "bash", "/app/utils/start_server.sh" ]
