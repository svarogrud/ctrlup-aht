#!/bin/bash

echo "Installing latest version of Python 3.13 and Allure reporting tool..."

if [[ "$(uname)" == "Darwin" ]]; then
  # Install Homebrew if not already installed
  if ! test -f "/usr/local/bin/brew"; then
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi

  # Install Python 3.13 and Allure using Homebrew
  brew install python@3.13 allure
elif [[ "$(uname)" == "Linux" ]]; then
  # Install Python 3.13 and Allure using apt-get for Debian/Ubuntu
  sudo apt-get update
  sudo apt-get install -y python3.13 python3.13-venv python3.13-dev allure
else
  echo "Error: unsupported operating system. Please install Python 3.13 manually."
  exit 1
fi

echo "Creating virtual env..."
python3.13 -m venv .pyvenv
echo "Installing python libs..."
.pyvenv/bin/pip3 install --no-cache -r requirements.txt
