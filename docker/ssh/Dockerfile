FROM ubuntu:18.04

# Install ssh
RUN apt update &&\
    apt install -y openssh-server

# Make workspace directory
RUN mkdir /workspace

# Setting /etc/ssh/ssd_config: PermitRootLogin prohibit-password -> yes
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config &&\
    sed -i 's/#StrictModes yes/StrictModes yes/' /etc/ssh/sshd_config &&\
    sed -i 's/#LoginGraceTime 2m/LoginGraceTime 120/' /etc/ssh/sshd_config

# Set root password
Run echo 'root:1qazxsw2@' | chpasswd

# Open port 22
EXPOSE 22

# Run service
#ENTRYPOINT ["service", "ssh", "start"]
CMD ["/usr/sbin/sshd", "-D"]

#https://dev.to/s1ntaxe770r/how-to-setup-ssh-within-a-docker-container-i5i

