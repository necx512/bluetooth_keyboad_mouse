# bluetooth_keyboad_mouse

sudo hciconfig hci0 up
sudo hcitool cmd 0x3f 0x001  0x54 0x32 0xfe 0x26 0xdb 0xc8
sudo hciconfig hci0 down
sudo hciconfig hci0 up

Ne pas oublier de supprimer tout device avec bluetoothctl ou par GUI
J'ai testé le client sous windows. Un client bluetoothctl semble pas marcher
