FROM thomergil/gpxmapmovie

ARG DEBIAN_FRONTEND=noninteractive
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn


ARG uid=1001
ARG gid=1001
RUN groupadd -g $gid trolleway && useradd --home /home/trolleway -u $uid -g $gid trolleway  \
  && mkdir -p /home/trolleway && chown -R trolleway:trolleway /home/trolleway
RUN echo 'trolleway:user' | chpasswd

RUN apt-get update  -y --allow-releaseinfo-change
#RUN apt full-upgrade
RUN apt-get install --no-install-recommends --fix-missing -y \
   openssh-server
	


RUN service ssh start
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
