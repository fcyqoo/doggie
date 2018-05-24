#!/bin/sh

apt-get update
apt-get -y dist-upgrade

# 创建代码目录
mkdir -p /var/www/assettool
chown -R www-data:www-data /var/www/assettool

# 创建日志目录
mkdir -p /mnt/log/assettool/
chown -R www-data:www-data /mnt/log
echo ">>>1"

# Install Nginx
apt-get install -y nginx
chown -R www-data:www-data /var/lib/nginx
chown -R www-data:www-data /var/log/nginx/
cp ./conf/nginx-site /etc/nginx/sites-available/default
cp ./conf/web_server/nginx-conf /etc/nginx/nginx.conf

# gunicorn
mkdir -p /mnt/run/assettool/
chown -R www-data /mnt/run/
mkdir -p /mnt/assettool/
chown -R www-data /mnt/
mkdir -p /mnt/log/gunicorn
chown -R www-data /mnt/log/

# Mysql
apt-get install -y mysql-client-5.7 libmysqlclient-dev
