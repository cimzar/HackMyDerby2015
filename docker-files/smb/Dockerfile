#FROM debian
FROM resin/rpi-raspbian

RUN apt-get -y update
RUN apt-get -y install samba 

EXPOSE 139

CMD ["/usr/sbin/smbd", "-F", "-S", "-s", "/smb/conf/smb.conf"]
