#FROM debian
FROM resin/rpi-raspbian

RUN apt-get -y update 
RUN apt-get -y update --fix-missing 
RUN apt-get -y install apache2 qrencode

EXPOSE 80
EXPOSE 443 

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
