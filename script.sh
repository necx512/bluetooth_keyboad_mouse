#!/bin/bash
sudo hciconfig hci0 up
sudo hciconfig hci0 piscan
sudo hciconfig hci0 name Logitech
sudo hcitool cmd 0x3f 0x001  0x54 0x32 0xfe 0x26 0xdb 0xc8
sudo hciconfig hci0 down
sudo hciconfig hci0 up
sudo hciconfig hci0 class 0x05C0
sudo hciconfig hci0 -a
