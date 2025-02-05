# bluetooth_keyboad_mouse

- sudo hciconfig hci0 up
- sudo hcitool cmd 0x3f 0x001  0x54 0x32 0xfe 0x26 0xdb 0xc8
- sudo hciconfig hci0 down
- sudo hciconfig hci0 up


Dans /etc/bluetooth/main.config:
Name = BlueZseb
Class = 0x05C0
DiscoverableTimeout = 0
PairableTimeout = 0



Ne pas oublier de supprimer tout device avec bluetoothctl ou par GUI
J'ai testé le client sous windows. Un client bluetoothctl semble pas marcher
[Unit]
Description=Bluetooth service
Documentation=man:bluetoothd(8)
ConditionPathIsDirectory=/sys/class/bluetooth

```
[Service]
Type=dbus
BusName=org.bluez
ExecStart=/usr/libexec/bluetooth/bluetoothd --noplugin=sap,vcp,mcp,bap,hostname
NotifyAccess=main
#WatchdogSec=10
#Restart=on-failure
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
LimitNPROC=1

# Filesystem lockdown
ProtectHome=true
ProtectSystem=strict
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
StateDirectory=bluetooth
StateDirectoryMode=0700
ConfigurationDirectory=bluetooth
ConfigurationDirectoryMode=0555

# Execute Mappings
MemoryDenyWriteExecute=true

# Privilege escalation
NoNewPrivileges=true

# Real-time
RestrictRealtime=true

[Install]
WantedBy=bluetooth.target
Alias=dbus-org.bluez.service
```

> sudo hciconfig -a
hci0:	Type: Primary  Bus: UART
	BD Address: B8:27:EB:4C:7B:E6  ACL MTU: 1021:8  SCO MTU: 64:1
	UP RUNNING PSCAN ISCAN 
	RX bytes:6394 acl:0 sco:0 events:384 errors:0
	TX bytes:37111 acl:0 sco:0 commands:384 errors:0
	Features: 0xbf 0xfe 0xcf 0xfe 0xdb 0xff 0x7b 0x87
	Packet type: DM1 DM3 DM5 DH1 DH3 DH5 HV1 HV2 HV3 
	Link policy: RSWITCH SNIFF 
	Link mode: PERIPHERAL ACCEPT 
	Name: 'BlueZseb'
	Class: 0x0005c0
	Service Classes: Unspecified
	Device Class: Peripheral, Combo keyboard/pointing device
	HCI Version: 4.1 (0x7)  Revision: 0x1fc
	LMP Version: 4.1 (0x7)  Subversion: 0x2209
	Manufacturer: Broadcom Corporation (15)

# Quelques commandes utiles
sudo hciconfig hci0 up
sudo hciconfig hci0 class 0x05C0
sudo hciconfig hci0 name
sudo hciconfig hci0 piscan
sudo /usr/libexec/bluetooth/bluetoothd


# remarques
Si les services dbus ET bluetooth doivent etre redemarrer, alors redemarrer dbus en premier.
