#!/bin/bash

# ***********
# on ubuntu *
# ***********

apt-get update

apt-get install -y nodejs npm
ln -s /usr/bin/nodejs /usr/bin/node

npm install -g phantomjs-prebuilt
