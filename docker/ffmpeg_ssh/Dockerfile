FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn


ARG uid=1001
ARG gid=1001
RUN groupadd -g $gid trolleway && useradd --home /home/trolleway -u $uid -g $gid trolleway  \
  && mkdir -p /home/trolleway && chown -R trolleway:trolleway /home/trolleway
RUN echo 'trolleway:password' | chpasswd


RUN apt-get update && apt-get install --no-install-recommends -y python3-pip time parallel imagemagick ffmpeg

#add to sudoers
RUN apt-get install -y apt-utils
RUN apt-get install -y sudo
RUN adduser trolleway sudo
RUN usermod -aG sudo trolleway



RUN apt install  openssh-server sudo  -y

RUN service ssh start
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]