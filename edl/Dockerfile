FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn

# NextGIS GDAL
RUN apt-get update -y && \
	apt-get -y install --no-install-recommends --yes python3 python3-pip  && \
	pip3 install --upgrade pip



ARG uid=1000
ARG gid=1000
RUN groupadd -g $gid trolleway && useradd --home /home/trolleway -u $uid -g $gid trolleway  \
  && mkdir -p /home/trolleway && chown -R trolleway:trolleway /home/trolleway
RUN echo 'trolleway:user' | chpasswd

#у меня в деревне такой инет, что сразу все зависимости не выкачиваются, и этот уровень завершается.
#попробую ставить зависимости по частям, чтоб меньше качать

RUN apt-get install --no-install-recommends -y time
RUN apt-get install --no-install-recommends -y ffmpeg

#add to sudoers
RUN apt-get install -y apt-utils
RUN apt-get install -y sudo
RUN adduser trolleway sudo
RUN usermod -aG sudo trolleway

WORKDIR /data/
#-p "$(openssl passwd -1 trolleway)"
