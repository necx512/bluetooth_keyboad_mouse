# configuration

Install the following package:

```
sudo apt install python3-bluez
sudo apt install build-essential
sudo apt install cmake
sudo apt install python3-dev
sudo apt install libdbus-1-dev
sudo apt install libdbus-glib-1-dev
```

In a venv:

```
pip3 install pybluez
pip3 install git+https://github.com/pybluez/pybluez.git#egg=pybluez
pip3 install dbus-python
```



In /etc/bluetooth/main.config, set the following variables:
```
Name = BlueZseb
Class = 0x05C0
DiscoverableTimeout = 0
PairableTimeout = 0
```

Ensure that the file `/lib/systemd/system/bluetooth.service` contains the following line:

`ExecStart=/usr/libexec/bluetooth/bluetoothd --noplugin=sap,vcp,mcp,bap,hostname,hid`

(Note: I'm not sure it is required to set hid in the previous line)

Then execute:
`
systemctl daemon-reload
systemctl disable bluetooth
systemctl stop bluetooth
`


# Lancement
```
sudo systemctl start bluetooth # pour appliquer la config qu'on a faite dans main.conf
sudo systemctl stop bluetooth # parce qu'on va lancer notre daemon minimal
sudo /usr/libexec/bluetooth/bluetoothd -p time # on lance notre daemon
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
