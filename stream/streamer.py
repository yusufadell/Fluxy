import base64
import sys
from dataclasses import dataclass

import cv2
import zmq

from stream.constants import *


@dataclass
class Streamer:
    server_address: str = SERVER_ADDRESS
    port: str = PORT
    socket: str = SOCKET

    def start(self, camera_mode=0):
        print(f"Connecting to {self.socket}")
        footage_socket = self.create_context()
        footage_socket.setsockopt_string(zmq.SUBSCRIBE, b"")
        print("Connected to server")
        self.send_frame(footage_socket)
        self.create_context()
        print("Streaming Started...")
        camera = cv2.VideoCapture(camera_mode)
        self.grab_frame(camera)

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
                grabbed, frame = camera.read()  # grab the current frame
                encoded, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer)
                self.footage_socket.send(jpg_as_text)

            except KeyboardInterrupt:
                camera.release()
                cv2.destroyAllWindows()
                break

    def __str__(self):
        return f"Streamer({self.server_address}, {self.port}, {self.socket})"


def main():
    port = PORT
    server_address = SERVER_ADDRESS

    try:
        if len(sys.argv) > 1:
            program_name = sys.argv[0]
            arguments = sys.argv[1:]
            count = len(arguments)
            server_address = arguments[0]
            port = arguments[1]
    except IndexError as ie:
        print("Loading default Server Address and Port.")

    streamer = Streamer()
    streamer.start()


if __name__ == '__main__':
    main()
