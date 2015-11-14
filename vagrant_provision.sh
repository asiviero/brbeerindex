#!/usr/bin/env bash

apt-get update
apt-get install -y git python-pip python-dev libxml2-dev libxslt1-dev gcc g++ liblz-dev libffi-dev libssl-dev polipo tor
sudo ln -s /lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so
sudo pip install scrapy --upgrade
sudo pip uninstall pyOpenSSL -y
sudo echo "socksParentProxy = localhost:9050" >> /etc/polipo/config
sudo echo 'diskCacheRoot=""' >> /etc/polipo/config
sudo /etc/init.d/polipo restartsudo pip install w3lib
sudo pip install future
sudo pip install numpy
sudo pip install dedupe
sudo pip install unidecode
