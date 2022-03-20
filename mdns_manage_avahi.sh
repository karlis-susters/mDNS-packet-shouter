#!/bin/bash
systemctl mask avahi-daemon.service
systemctl kill avahi-daemon.service
python ./mdns.py
systemctl unmask avahi-daemon.service
systemctl restart avahi-daemon.service

