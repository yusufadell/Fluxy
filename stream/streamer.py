import argparse
import base64
from dataclasses import dataclass

import cv2
import zmq
import typing
from constants import *
from camera.Camera import Camera


@dataclass
class Streamer:
    server_address: str = SERVER_ADDRESS
    port: str = PORT
    socket: str = SOCKET
    camera: typing.Any = Camera()

    def start(self):
        print(f"Connecting to {self.socket}")
        footage_socket = self.create_context()
        footage_socket.setsockopt_string(zmq.SUBSCRIBE, b"")
        print("Connected to server")
        self.send_frame(footage_socket)
        self.create_context()
        print("Streaming Started...")
        self.camera.start_capture()
        self.grab_frame(self.camera)

    def create_context(self):
        context = zmq.Context()
        footage_socket = context.socket(zmq.SUB)
        footage_socket.connect(self.socket)
        return footage_socket

    def send_frame(self, footage_socket):
        while True:
            try:
                frame = footage_socket.recv_string()
                frame = base64.b64decode(frame)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                cv2.imshow("Stream", frame)
                cv2.waitKey(1)
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break

    def grab_frame(self, camera):
        while self.footage_socket:
            try:
                frame = camera.current_frame.read()
                jpg_as_text = self._image_to_string(frame)
                self.footage_socket.send(jpg_as_text)

            except KeyboardInterrupt:
                camera.release()
                cv2.destroyAllWindows()
                break

    def __str__(self):
        return f"Streamer({self.server_address}, {self.port}, {self.socket})"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--port', help='The port which you want the Streaming Viewer to use, default'' is ' + PORT, required=False)
    args = parser.parse_args()
    if args.port:
        port = args.port
    streamer = Streamer(port=port)
    streamer.start()
