#!/bin/bash

pip install websocket_client
pip install pyserial
pip install json
pip install boto3

chmod +x *.py
cp rc.local /etc/

read -p "Raspberry Pi Needs To Be Rebooted For Changes To Take Effect! " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    reboot
fi

exit 0