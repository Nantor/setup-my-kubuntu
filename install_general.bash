#!/bin/bash

## update system
sudo apt update
sudo apt -y upgrade

## install packs
sudo apt -y install git gcc perl make gimp apt-transport-https ca-certificates software-properties-common filezilla openjdk-11-jdk openjdk-11-source update-manager snap python3-distutils

## install nodejs
curl -sL https://deb.nodesource.com/setup_11.x | sudo -E bash -

## snap install apps
sudo snap install chromium
sudo snap install firefox
sudo snap install pycharm-community --classic
sudo snap install intellij-idea-ultimate --classic
sudo snap install vscode --classic
sudo snap install docker

## clean up
sudo apt update
sudo apt -y upgrade
sudo apt -y autoremove
sudo apt -y autoclean
