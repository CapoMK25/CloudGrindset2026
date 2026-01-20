# a very basic provisioning script to set up NGINX web server on a Linux VM/WSL/machine

#!/bin/bash

apt update

apt install -y nginx

systemctl enable nginx

systemctl start nginx