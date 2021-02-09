#!/usr/bin/env sh
apt-get install gettext-base # required for envsubst
envsubst < config.tmpl > config.json

