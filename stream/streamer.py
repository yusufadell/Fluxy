import argparse
import base64
import typing
from dataclasses import dataclass

import cv2
import zmq
from camera.Camera import Camera
from constants import *
from utils import image_to_string


@dataclass
class Streamer:
    """
    Tries to connect to the StreamViewer with supplied server_address and creates a socket for future use.

    :param server_address: Address of the computer on which the StreamViewer is running, default is `localhost`
    :param port: Port which will be used for sending the stream
    """

    port: str = PORT
    server_address: str = SERVER_ADDRESS
    socket: str = SOCKET
    camera: typing.Any = Camera()
    camera.start_capture()

    def start(self):
        """
        Starts sending the stream to the Viewer.
        Creates a camera, takes a image frame converts the frame to string and sends the string across the network
        :return: None
        """
        print(f"Connecting to {self.socket}")
        footage_socket = self.create_context()
        footage_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        print("Connected to server")
        self.send_frame(footage_socket)
        self.create_context()
        print("Streaming Started...")
        self.grab_frame(self.camera)

    def create_context(self):
        context = zmq.Context()
        footage_socket = context.socket(zmq.SUB)
        footage_socket.connect(self.socket)
        return footage_socket

    def send_frame(self, footage_socket):
        """send_frame sends the frame to the server

        :param footage_socket: Socket to which the frame will be sent 
        :type footage_socket: zmq.Socket 
        """
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
        """grab_frame takes a frame from the camera and sends it to the server

        :param camera: Camera object from which the frame will be taken
        :type camera: Camera
        """
        while self.footage_socket:
            try:
                frame = camera.current_frame.read()
                jpg_as_text = image_to_string(frame)
                self.footage_socket.send(jpg_as_text)

            except KeyboardInterrupt:
                camera.release()
                cv2.destroyAllWindows()
                break

    def __str__(self):
        """__str__ returns the string representation of the object

        :return: String representation of the object
        :rtype: str
        """
        return f'Subsriber rule at port:{self.port}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--port', help='The port which you want the Streaming Viewer to use, default'' is ' + PORT, required=False)
    args = parser.parse_args()
    if args.port:
        port = args.port
    streamer = Streamer(port=port)
    streamer.start()
