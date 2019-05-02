#!/bin/bash

# Fail on any bash command failure
set -e


function install_python36 () {
    echo "Installing Python 3.6..."
    sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt-get update
    sudo apt-get -y install libssl-dev libxss1 libappindicator1 libindicator7 libappindicator3-1
    sudo apt-get -y install python3.6 python3-pip
    echo "Finished install Python 3.6."
}

function install_chrome_utils () {
    echo "Installing Google Chrome stable..."
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i google-chrome*.deb
    echo "Installing Chromedriver..."
    sudo apt-get -y install -f
    sudo apt-get install xvfb
    sudo rm -f chromedriver chromedriver_linux64.zip ~/bin/chromedriver /usr/bin/chromedriver /usr/local/bin/chromedriver
    wget https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip && chmod +x chromedriver
    sudo mv -f chromedriver /usr/local/share/chromedriver
    sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
    sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
    echo "Finished installing Chrome and Chromedriver."
}

function setup_venv () {
    sudo mv .circleci/Arial.ttf /usr/share/fonts
    docker login -u $DOCKERHUB_USER -p $DOCKERHUB_PASSWORD
    sudo apt-get -y install python3.6-venv
}

install_python36
install_chrome_utils
setup_venv
