#!/bin/bash

pip install -r requirements.txt

install -m 0755 collector/goaccess-tui.service /etc/systemd/system/goaccess-tui.service
install -m 0755 collector/goaccess-tui.timer /etc/systemd/system/goaccess-tui.timer

systemctl daemon-reload

systemctl enable goaccess-tui.service
systemctl enable goaccess-tui.timer

systemctl restart goaccess-tui.service
systemctl restart goaccess-tui.timer
