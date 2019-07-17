import sys
# Add parent folder to path so that the API can be imported.
# This shouldn't be required if the package has been installed via pip
sys.path.insert(0, '../')
sys.path.insert(0, '../cflib/')

import struct
import time

import cflib
import cflib.crazyflie
from cflib.crtp.crtpstack import CRTPPacket
from cflib.crtp.crtpstack import CRTPPort


def scan_for_crazyflies():
    cflib.crtp.init_drivers()
    available = cflib.crtp.scan_interfaces()
    return available


def incoming(packet):
    """
    Callback for data received from the copter.
    """
    # This might be done prettier ;-)
    print("Message received:")
    print("Header: " + str(packet.header))
    print("Data: " + str(struct.unpack('<f', packet.data)[0]))
    print("\n")

if __name__ == "__main__":
    cfies = scan_for_crazyflies()
    cf = cflib.crazyflie.Crazyflie(rw_cache='./cache')
    cf.add_port_callback(CRTPPort.SENSOR, incoming)
    cf.open_link(cfies[0][0])
    print("Link opened\n")
    # Create sensor packet
    pk = CRTPPacket()
    pk.port = CRTPPort.SENSOR
    pk.data = struct.pack('<B', 1)
    print("Sending message:")
    print("Header: " + str(pk.header))
    print("Data: " + str(pk.data))
    print("\n")
    cf.send_packet(pk)
    time.sleep(1)
    cf.close_link()
