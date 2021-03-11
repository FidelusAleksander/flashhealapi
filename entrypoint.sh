#!/bin/bash
envsubst < config.tmpl > config.json
python /opt/flashhealapi/app.py
