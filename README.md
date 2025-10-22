# configuration

Install the following package:

```
sudo apt install python3-bluez build-essential cmake python3-dev libdbus-1-dev libdbus-glib-1-dev libbluetooth-dev
```

In a venv:

```
python3 -m venv venv
source venv/bin/activate
pip3 install pybluez # not required?
pip3 install git+https://github.com/pybluez/pybluez.git#egg=pybluez
pip3 install dbus-python
```



In /etc/bluetooth/main.conf, set the following variables:
```
Name = Logitech
Class = 0x05C0
DiscoverableTimeout = 0
PairableTimeout = 0
```

Ensure that the file `/lib/systemd/system/bluetooth.service` contains the following line:

`ExecStart=/usr/libexec/bluetooth/bluetoothd --plugin=time`

Setting time plugin prevent other plugin to run. For instance, the plugin 'hostname' give the name of the machine to the name of the bluetooth device and we don't want it.
Another exemple is the use of some L2CAP ports that we want by some plugins.
Perhaps we can replace 'time' by a random string?

Then execute:
`
systemctl daemon-reload
systemctl enable bluetooth
systemctl restart bluetooth
hciconfig hci0 up
`

If you get the error "Can't init device hci0: Operation not possible due to RF-kill (132)":
1. rfkill list
2. sudo rfkill unblock bluetooth


# Lancement
With bluetoothctl and the command 'paired-devices', make sure that there is no device. if there is, remove it by command `remove`

```
sudo hciconfig hci0 up # because 'systemctl stop bluetooth' a arreter l'interface
```

La command `hciconfig -a` doit faire aparaitre `UP RUNNING PSCAN ISCAN`, 'Name: 'BlueZseb' et 'Class: 0x0005c0'



# Quelques commandes utiles
## voir les interfaces
sudo hciconfig -a

## Demarrer / arreter l'interface
sudo hciconfig hci0 up
sudo hciconfig hci0 down

## Changer la classe
sudo hciconfig hci0 class 0x05C0
sudo hciconfig hci0 name

## Mettre en ecoute (est ce que ca implique discoverable et pairable comme configurer dans main.conf?)
sudo hciconfig hci0 piscan

## changer la mac (peut necessité de redemarrer l'interface)
sudo hcitool cmd 0x3f 0x001  0x54 0x32 0xfe 0x26 0xdb 0xc8

## dbus commands
busctl

# remarques
Si les services dbus ET bluetooth doivent etre redemarrer, alors redemarrer dbus en premier.

# Troubleshooting  for already used
sudo lsof -nP | grep -i bluetooth
sudo lsof -nP | grep -i l2cap


# old README.md

- sudo hciconfig hci0 up
- sudo hciconfig hci0 down
- sudo hciconfig hci0 up

Ne pas oublier de supprimer tout device avec bluetoothctl ou par GUI
J'ai testé le client sous windows. Un client bluetoothctl semble pas marcher



===
seb@logitech:~/bluetooth_keyboad_mouse $ sudo hciconfig -a
hci0:	Type: Primary  Bus: UART
	BD Address: C8:DB:26:FE:32:54  ACL MTU: 1021:8  SCO MTU: 64:1
	UP RUNNING PSCAN ISCAN 
	RX bytes:21910 acl:98 sco:0 events:867 errors:0
	TX bytes:47557 acl:92 sco:0 commands:776 errors:0
	Features: 0xbf 0xfe 0xcf 0xfe 0xdb 0xff 0x7b 0x87
	Packet type: DM1 DM3 DM5 DH1 DH3 DH5 HV1 HV2 HV3 
	Link policy: RSWITCH SNIFF 
	Link mode: PERIPHERAL ACCEPT 
	Name: 'Logitech'
	Class: 0x6005c0
	Service Classes: Audio, Telephony
	Device Class: Peripheral, Combo keyboard/pointing device
	HCI Version: 4.1 (0x7)  Revision: 0x1fc
	LMP Version: 4.1 (0x7)  Subversion: 0x2209
	Manufacturer: Broadcom Corporation (15)

===
Ne pas oublier de lire les log : systemctl status bluetooth
