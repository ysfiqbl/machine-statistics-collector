# Using official python runtime base image
FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python-pip python-dev build-essential openssh-server gcc
RUN pip install --upgrade pip
RUN pip install --upgrade virtualenv

RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

# Set the application directory
WORKDIR /tmp

# Install our requirements.txt
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r requirements.txt