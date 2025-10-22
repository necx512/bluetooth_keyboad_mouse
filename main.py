import sys
import os
import dbus
import time
import traceback
import keymap
import bluetooth
import dbus.service
import dbus.mainloop.glib
import random
import uuid
from dbus.mainloop.glib import DBusGMainLoop


class BluetoothBluezProfile(dbus.service.Object):
    fd = -1

    @dbus.service.method("org.bluez.Profile1", in_signature="", out_signature="")
    def Release(self):
        print("Release")
        exit(-1)

    @dbus.service.method("org.bluez.Profile1",
                         in_signature="", out_signature="")
    def Cancel(self):
        print("Cancel")

    @dbus.service.method("org.bluez.Profile1", in_signature="oha{sv}", out_signature="")
    def NewConnection(self, path, fd, properties):
        self.fd = fd.take()
        print("NewConnection(%s, %d)" % (path, self.fd))
        for key in properties.keys():
            if key == "Version" or key == "Features":
                print("  %s = 0x%04x" % (key, properties[key]))
            else:
                print("  %s = %s" % (key, properties[key]))

    @dbus.service.method("org.bluez.Profile1", in_signature="o", out_signature="")
    def RequestDisconnection(self, path):
        print("RequestDisconnection(%s)" % (path))

        if (self.fd > 0):
            os.close(self.fd)
            self.fd = -1

    def __init__(self, bus, path):
        dbus.service.Object.__init__(self, bus, path)


# create a bluetooth device to emulate a HID keyboard/mouse,
# advertize a SDP record using our bluez profile class
#
class BTDevice:
    BT_ADDRESS = "C8:DB:26:FE:32:54"
    #BT_ADDRESS = bluetooth.read_local_bdaddr()[0]

    BT_DEV_NAME = "Logitech"

    # define some constants
    P_CTRL = 17  # Service port - must match port configured in SDP record
    P_INTR = 19  # Service port - must match port configured in SDP record #Interrrupt port
    PROFILE_DBUS_PATH = "/bluez/hzy/hidbluetooth_profile"  # dbus path of the bluez profile we will create
    SDP_RECORD_PATH = "/home/seb/bluetooth_keyboad_mouse/sdp_recordv1.xml"  # file path of the sdp record to load
    UUID = "00001124-0000-1000-8000-00805f9b34fb"
    #UUID = str(uuid.uuid4())

    def __init__(self):

        print("Setting up Bluetooth device")
        self.init_bt_device()
        self.init_bluez_profile()

    # configure the bluetooth hardware device
    def init_bt_device(self):


        register_agent()

    # set up a bluez profile to advertise device capabilities from a loaded service record
    def init_bluez_profile(self):
        print("Configuring Bluez Profile")

        # setup profile options
        service_record = self.read_sdp_service_record()

        opts = {
            "ServiceRecord": service_record,
            "Role": "server",
            "RequireAuthentication": False,
            "RequireAuthorization": False
        }

        # retrieve a proxy for the bluez profile interface
        bus = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object("org.bluez", "/org/bluez"), "org.bluez.ProfileManager1")

        profile = BluetoothBluezProfile(bus, self.PROFILE_DBUS_PATH)

        try:
            manager.UnregisterProfile(self.PROFILE_DBUS_PATH)
            print("Profile removed")
        except:
            print("No profile exist")

        manager.RegisterProfile(self.PROFILE_DBUS_PATH, self.UUID, opts)

        print("Profile registered ")

    # read and return an sdp record from a file
    def read_sdp_service_record(self):

        print("Reading service record")

        try:
            fh = open(self.SDP_RECORD_PATH, "r")
        except Exception as e:
            traceback.print_exc()
            print(e)
            sys.exit("Could not open the sdp record. Exiting...")

        return fh.read()

    # listen for incoming client connections

    # ideally this would be handled by the Bluez 5 profile
    # but that didn't seem to work
    def listen(self):

        print("Waiting for connections")
        self.scontrol = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        self.sinterrupt = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        print("bind...")
        # bind these sockets to a port - port zero to select next available
        self.scontrol.bind((self.BT_ADDRESS, self.P_CTRL))
        self.sinterrupt.bind((self.BT_ADDRESS, self.P_INTR))
        # Start listening on the server sockets
        print("listen...")
        self.scontrol.listen(1)  # Limit of 1 connection
        self.sinterrupt.listen(1)
        print("ready to accept...")
        self.ccontrol, cinfo = self.scontrol.accept()
        print("Got a connection on the control channel from " + cinfo[0])

        self.cinterrupt, cinfo = self.sinterrupt.accept()
        print("Got a connection on the interrupt channel from " + cinfo[0])

    # send a string to the bluetooth host machine
    def send_string(self, message):
        self.cinterrupt.send(message)

    def close(self):
        self.scontrol.close()
        self.sinterrupt.close()

    def send_keys(self, modifier_byte, keys):
        cmd_bytes = bytearray()
        cmd_bytes.append(0xA1)
        cmd_bytes.append(0x01)  # report id
        cmd_bytes.append(modifier_byte)
        cmd_bytes.append(0x00)
        assert len(keys) == 6
        for key_code in keys:
            cmd_bytes.append(key_code)

        self.send_string(bytes(cmd_bytes))

    def send_mouse(self, buttons, rel_move):
        cmd_bytes = bytearray()
        cmd_bytes.append(0xA1)
        cmd_bytes.append(0x02)  # report id
        cmd_bytes.append(buttons)
        cmd_bytes.append(rel_move[0])
        cmd_bytes.append(rel_move[1])
        cmd_bytes.append(rel_move[2])
        self.send_string(bytes(cmd_bytes))


def send_string(device, string, key_down_time=0.01, key_delay=0.05):
    for c in string:
        key = 'KEY_' + c.upper()
        if key in keymap.keytable:
            code = keymap.keytable[key]
            device.send_keys(0, [code, 0, 0, 0, 0, 0])
            time.sleep(key_down_time)
            device.send_keys(0, [0, 0, 0, 0, 0, 0])
            time.sleep(key_delay)


def register_agent():
    bus = dbus.SystemBus()

    # Define the agent path (choose an arbitrary path)
    agent_path = "/test/agent"

    # Get the agent manager interface
    agent_manager = dbus.Interface(
        bus.get_object("org.bluez", "/org/bluez"),
        "org.bluez.AgentManager1"
    )

    # Register the agent with NoInputNoOutput capability
    agent_manager.RegisterAgent(agent_path, "NoInputNoOutput")
    agent_manager.RequestDefaultAgent(agent_path)

    print("Agent registered and set as default")



def main():


    timerandom = random.randint(2,60)
    xrandom = random.randint(10,100)
    yrandom = random.randint(10,100)
    if not os.geteuid() == 0:
        sys.exit("Only root can run this script")
    print("restart bluetooth")
    DBusGMainLoop(set_as_default=True)
    device = BTDevice()
    device.listen()
    print("init success")
    while True:
        timerandom = random.randint(2,60)
        xrandom = random.randint(10,100)
        yrandom = random.randint(10,100)
        time.sleep(timerandom) # do random between 2 and 60
        device.send_mouse(0, [xrandom, yrandom, 1])
        #v = input("input str>>>")
        #if v == 'q':
        #    break
        #elif v == 'm':
        #    print("send mouse")
        #    device.send_mouse(0, [10, 30, 1])
        #else:
        #    print('send:', v)
        #    send_string(device, v)


if __name__ == '__main__':
    main()
