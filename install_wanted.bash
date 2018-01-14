sudo usermod -aG docker#!/bin/bash

## update system
sudo apt update
sudo apt -y upgrade

## install packs
sudo apt -y install git gcc perl make chromium-browser firefox curl gimp apt-transport-https ca-certificates software-properties-common

## install docker
curl -fsSL get.docker.com | sudo sh
sudo usermod -aG docker $(whoami)

## install nodejs
#wget -qO- https://deb.nodesource.com/setup_9.x | sudo -E bash -
#sudo apt-get install -y nodejs
#mkdir ~/.npm-global
#npm config set prefix '~/.npm-global'
#echo "" > ~/.profile
#echo "export PATH=~/.npm-global/bin:\$PATH" > ~/.profile
#source ~/.profile

## install Visual Studio Code
vsc_tmp=$(mktemp)
wget -O $vsc_tmp https://go.microsoft.com/fwlink/?LinkID=760868
sudo dpkg -i $vsc_tmp
sudo apt-get install -f

## install JetBrains PyCharm
wget -O $vsc_tmp $(curl -s 'https://data.services.jetbrains.com/products/releases?code=PCC&latest=true&type=release' | python3 -c "import sys, json; print(json.load(sys.stdin)['PCC'][0]['downloads']['linux']['link'])")
sudo tar xf $vsc_tmp -C /opt/
sudo ln -s /opt/pycharm-community-*/bin/pycharm.sh /usr/bin/pycharm

## clean up
sudo apt update
sudo apt -y upgrade
sudo apt -y autoremove
sudo apt -y autoclean
