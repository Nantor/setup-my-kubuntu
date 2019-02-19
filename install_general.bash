#!/bin/bash

## update system
sudo apt update
sudo apt -y upgrade

## install packs
sudo apt -y install git gcc g++ perl make gimp apt-transport-https ca-certificates software-properties-common filezilla openjdk-11-jdk openjdk-11-source update-manager snap python3-distutils firefox curl

## install nodejs
curl -sL https://deb.nodesource.com/setup_11.x | sudo -E bash -
sudo apt-get install -y nodejs

## install yarn
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update && sudo apt-get install yarn

## snap install apps
sudo snap install chromium --classic
sudo snap install pycharm-community --classic
sudo snap install intellij-idea-ultimate --classic
sudo snap install vscode --classic
sudo snap install docker

## clean up
sudo apt update
sudo apt -y upgrade
sudo apt -y autoremove
sudo apt -y autoclean
