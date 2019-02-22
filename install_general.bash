#!/bin/bash

## install nodejs
curl -sL https://deb.nodesource.com/setup_11.x | sudo -E bash -

## install yarn
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

## install packs
sudo apt update
sudo apt -y install git gcc g++ perl make gimp apt-transport-https ca-certificates software-properties-common filezilla openjdk-11-jdk openjdk-11-source update-manager snap python3-distutils firefox yarn nodejs

## snap install apps
sudo snap install chromium --classic
sudo snap install pycharm-community --classic
sudo snap install intellij-idea-ultimate --classic
sudo snap install vscode --classic
sudo snap install docker

## update system
sudo apt update
sudo apt -y upgrade

## clean up
sudo apt -y autoremove
sudo apt -y autoclean
