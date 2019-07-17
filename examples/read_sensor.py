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
    """
    Scan for available crazyflies
    """
    cflib.crtp.init_drivers()
    available = cflib.crtp.scan_interfaces()
    return available

def incoming(packet):
    """
    Callback for data received from the copter. This gets
    called when a message from SENSOR port is received
    """
    # This might be done prettier ;-)
    print("Message received:")
    print("Header: " + str(packet.header))
    # We know that the current answer is a float so
    # this unpack shouldn't fail.
    print("Data: " + str(struct.unpack('<f', packet.data)[0]))
    print("\n")

def main():
    found_cfies = scan_for_crazyflies()
    # Create Crazyflie instance
    cf = cflib.crazyflie.Crazyflie(rw_cache='./cache')
    cf.add_port_callback(CRTPPort.SENSOR, incoming)
    # Connect to the first detected crazyflie
    # found_cfies[0][0] contains the uri of the drone
    cf.open_link(found_cfies[0][0])
    print("Link opened\n")
    # Create packet aimed at the SENSOR port
    pk = CRTPPacket()
    pk.port = CRTPPort.SENSOR
    # Fill it with dummy data. Eventually this should
    # be changed by the ID of the sensor
    pk.data = struct.pack('<B', 1)
    print("Sending message:")
    print("Header: " + str(pk.header))
    print("Data: " + str(pk.data))
    print("\n")
    cf.send_packet(pk)
    time.sleep(1) # Wait to receive answer
    # Incoming messages are received and processed in a different
    # thread. See the _IncomingPacketHandler class at cflib/crazyflie/__init__.py 
    cf.close_link()

if __name__ == "__main__":
    main()
