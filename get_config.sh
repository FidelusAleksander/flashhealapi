#!/usr/bin/env sh
sudo apt-get install gettext-base # required for envsubst
envsubst < config.tmpl > config.json

