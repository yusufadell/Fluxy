import argparse
import base64
import sys
import typing
from dataclasses import dataclass

import cv2
import numpy as np
import zmq

from constants import *


@dataclass
class StreamViewer:
    """
    Tries to connect to the StreamViewer with supplied server_address and creates a socket for future use.
    """
    port: str = PORT
    server_address: str = SERVER_ADDRESS
    display: bool = True
    context: typing.Any = zmq.Context()
    footage_socket: typing.Any = context.socket(zmq.SUB)

    def decode_frames(self):
        """decode_frames decodes the frames received from the server
        :return: None
        """
        frame = self.footage_socket.recv_string()
        img = base64.b64decode(frame)
        npimg = np.fromstring(img, dtype=np.uint8)
        self.current_frame = cv2.imdecode(npimg, 1)
        if self.display:
            cv2.imshow('Stream', self.current_frame)
            cv2.waitKey(1)

    def listen(self):
        """start listening for incoming stream frames from the server
        """
        self.footage_socket.bind(f'tcp://*:{PORT}')
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, '')
        print(f"Listening for stream... port:{self.port} press ctrl+c to exit")
        while self.footage_socket:
            try:
                self.decode_frames()
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break

    def __str__(self):
        return f'Subsriber rule at port:{self.port}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--server', help='IP Address of the server which you want to connect to, default'' is ' + SERVER_ADDRESS, required=True)
    parser.add_argument(
        '-p', '--port', help='The port which you want the Streaming Server to use, default'' is ' + PORT, required=False)

    args = parser.parse_args()

    if args.port and args.server:
        port, addr = args.port, args.server

    streamer = StreamViewer(port=port, server_address=addr)
    streamer.listen()
