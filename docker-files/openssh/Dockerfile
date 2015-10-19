#FROM debian
FROM resin/rpi-raspbian

RUN apt-get -y update --fix-missing
RUN apt-get -y install openssh-server python
RUN useradd hackme -m -d /home/hackme
RUN usermod -p '$6$Uzc1kGVl$GVAm3QQd5/HZGzIUCiJ6Ukyd37MBawy7FZHybUrAWOYruwlLL0hE1buBDThmR5WA0pz2olbz092COkQDZyr7L0' hackme
RUN mkdir /var/run/sshd

COPY ./runme.sh /home/hackme/runme.sh

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
