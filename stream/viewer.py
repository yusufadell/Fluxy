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
    port: str = PORT
    context: typing.Any = zmq.Context()
    footage_socket: typing.Any = context.socket(zmq.SUB)
    footage_socket.bind(f'tcp://*:{PORT}')
    footage_socket.setsockopt_string(zmq.SUBSCRIBE, '')

    def listen(self):
        """start listening for incoming stream
        """
        print(f"Listening for stream... port:{self.port} press ctrl+c to exit")
        while self.footage_socket:
            try:
                self.decode_frames()
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break

    def decode_frames(self):
        frame = self.footage_socket.recv_string()
        img = base64.b64decode(frame)
        npimg = np.fromstring(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        cv2.imshow("Stream", source)
        cv2.waitKey(1)

    def __str__(self):
        return f'Subsriber rule at port:{self.port}'


if __name__ == '__main__':
    streamer = StreamViewer()
    streamer.listen()
