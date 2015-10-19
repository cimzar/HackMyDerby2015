FROM debian
#FROM resin/rpi-raspbian

# Install packages
RUN apt-get -y update --fix-missing
RUN apt-get -y install openssh-server python sudo

# add our idiot network engineer
RUN useradd hackme -m -d /home/hackme
RUN usermod -p '$6$Uzc1kGVl$GVAm3QQd5/HZGzIUCiJ6Ukyd37MBawy7FZHybUrAWOYruwlLL0hE1buBDThmR5WA0pz2olbz092COkQDZyr7L0' hackme
RUN echo "hackme	ALL=/var/secret/runme.sh" >> /etc/sudoers

# Do something dumb, for contestants to find.
RUN chmod o+r /etc/sudoers

# Get sshd in order
RUN mkdir /var/run/sshd
RUN sed -i 's/Subsystem sftp/#Subsystem sftp/' /etc/ssh/sshd_config
RUN echo "ForceCommand           /bin/sh" >> /etc/ssh/sshd_config
RUN echo "AllowTcpForwarding     no" >> /etc/ssh/sshd_config
RUN echo "PermitTunnel           no" >> /etc/ssh/sshd_config
RUN echo "PermitUserEnvironment  no" >> /etc/ssh/sshd_config

# Get the flag environment in order
RUN mkdir /var/secret
COPY ./runme.sh /home/hackme/runme.sh
COPY ./runme.sh /var/secret/runme.sh
RUN chmod 555 /home/hackme/runme.sh
RUN chmod 555 -R /var/secret

# SSH needs port 22
EXPOSE 22

# ssh needs a daemon
CMD ["/usr/sbin/sshd", "-D"]
