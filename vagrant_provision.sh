#!/usr/bin/env bash

apt-get update
apt-get install -y git python-pip python-dev libxml2-dev libxslt1-dev gcc g++ liblz-dev libffi-dev libssl-dev polipo tor
#pip install cython
sudo ln -s /lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so
# sudo pip uninstall -y scrapy
sudo pip install scrapy --upgrade
sudo pip uninstall pyOpenSSL -y
sudo echo "socksParentProxy = localhost:9050" >> /etc/polipo/config 
sudo echo 'diskCacheRoot=""' >> /etc/polipo/config 
sudo /etc/init.d/polipo restartsudo pip install w3lib
#sudo pip install lxml
#pip3 install django==1.8
#pip3 install --upgrade selenium
#pip3 install factory_boy
#pip3 install fake-factory
#pip3 install Pillow
#pip3 install django-material
#pip3 install python-dateutil
#pip3 install django-allauth
#pip3 install djangoajax
#pip3 install celery
#pip3 install redis
#pip3 install django-appconf
#pip3 install django-guardian
