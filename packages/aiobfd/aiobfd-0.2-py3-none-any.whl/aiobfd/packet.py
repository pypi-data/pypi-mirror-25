"""aiobfd: BFD Control Packet"""
# pylint: disable=I0011,E0632,R0902

import logging
import bitstring
log = logging.getLogger(__name__)  # pylint: disable=I0011,C0103

MIN_PACKET_SIZE = 24
MIN_AUTH_PACKET_SIZE = 26
STATE_ADMIN_DOWN = 0                # AdminDown
STATE_DOWN = 1                      # Down

'''
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Vers |  Diag   |Sta|P|F|C|A|D|M|  Detect Mult  |    Length     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       My Discriminator                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Your Discriminator                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Desired Min TX Interval                    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                   Required Min RX Interval                    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 Required Min Echo RX Interval                 |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''

PACKET_FORMAT = (
    'uint:3=version,'
    'uint:5=diag,'
    'uint:2=state,'
    'bool=poll,'
    'bool=final,'
    'bool=control_plane_independent,'
    'bool=authentication_present,'
    'bool=demand_mode,'
    'bool=multipoint,'
    'uint:8=detect_mult,'
    'uint:8=length,'
    'uint:32=my_discr,'
    'uint:32=your_discr,'
    'uint:32=desired_min_tx_interval,'
    'uint:32=required_min_rx_interval,'
    'uint:32=required_min_echo_rx_interval'
)

PACKET_DEBUG_MSG = '\n|--------------------------------------------------\n' \
                   '| Vers: %d Diag: %d State: %d Poll: %d Final: %d\n' \
                   '| CPI: %d Auth: %d Demand: %d Multi: %d DetectMult: %d\n' \
                   '| Length: %d MyDisc: %d YourDisc: %d\n' \
                   '| TxInterval: %d RxInterval: %d EchoRxInterval: %d\n' \
                   '|--------------------------------------------------'


class Packet:  # pylint: disable=I0011,R0903
    """A BFD Control Packet"""

    def __init__(self, data, source):
        self.source = source

        packet = bitstring.BitString(data)
        packet_length = packet.len / 8
        # Ensure packet is sufficiently long to attempt unpacking it

        if packet_length < MIN_PACKET_SIZE:
            raise IOError('Packet size below mininum correct value.')

        self.version, self.diag, self.state, self.poll, self.final, \
            self.control_plane_independent, self.authentication_present,\
            self.demand_mode, self.multipoint, self.detect_mult, self.length, \
            self.my_discr, self.your_discr, self.desired_min_tx_interval, \
            self.required_min_rx_interval, self.required_min_echo_rx_interval \
            = packet.unpack(PACKET_FORMAT)

        log.debug(PACKET_DEBUG_MSG, self.version, self.diag, self.state,
                  self.poll, self.final, self.control_plane_independent,
                  self.authentication_present, self.demand_mode,
                  self.multipoint, self.detect_mult, self.length,
                  self.my_discr, self.your_discr, self.desired_min_tx_interval,
                  self.required_min_rx_interval,
                  self.required_min_echo_rx_interval)

        self.validate(packet_length)

    def validate(self, packet_length):
        """Validate received packet contents"""

        # If the version number is not correct (1), the packet MUST be
        # discarded.
        if self.version != 1:
            raise IOError('Unsupported BFD protcol version.')

        # If the Length field is less than the minimum correct value (24 if
        # the A bit is clear, or 26 if the A bit is set), the packet MUST be
        # discarded.
        if self.authentication_present and self.length < MIN_AUTH_PACKET_SIZE:
            raise IOError('Packet size below mininum correct value.')
        elif ((not self.authentication_present)
              and self.length < MIN_PACKET_SIZE):
            raise IOError('Packet size below mininum correct value.')

        # If the Length field is greater than the payload of the encapsulating
        # protocol, the packet MUST be discarded.
        if self.length > packet_length:
            raise IOError('Packet length field larger than received data.')

        # If the Multipoint (M) bit is nonzero, the packet MUST be discarded.
        if self.multipoint:
            raise IOError('Multipoint bit should be 0.')

        # If the My Discriminator field is zero, the packet MUST be discarded.
        if not self.my_discr:
            raise IOError('Discriminator field is zero.')

        # If the Your Discriminator field is zero and the State field is not
        # Down or AdminDown, the packet MUST be discarded.
        if self.state not in [STATE_DOWN, STATE_ADMIN_DOWN] \
           and (not self.your_discr):
            raise IOError('Your Discriminator can\'t be zero in this state.')
