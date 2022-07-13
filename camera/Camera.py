import time

from constants import *
from utils import preview_image


class Camera:

    def __init__(self, height=RESOLUTION_H, width=RESOLUTION_W):
        self.current_frame = None
        self.height = height
        self.width = width
        self.camera = None

    def start_capture(self, height=None, width=None, usingPiCamera=IS_RASPBERRY_PI, ):
        import imutils
        from imutils.video import VideoStream
        resolution = (self.height, self.width)
        if height:
            if width:
                resolution = (height, width)
        cf = VideoStream(usePiCamera=usingPiCamera,
                         resolution=resolution, framerate=32).start()
        self.current_frame = cf
        time.sleep(2)

        if not usingPiCamera:
            frame = imutils.resize(
                self.current_frame.read(), width=resolution[0])

    def stop_capture(self):
        print("Stopping Capture")
        self.current_frame.stop()

    def capture_image(self):
        import cv2

        ramp_frames = 30

        self.camera = cv2.VideoCapture(CAMERA_PORT)
        _, im = self.camera.read()
        [self.camera.read() for _ in range(ramp_frames)]
        print("Taking image...")
        _, camera_capture = self.camera.read()
        del self.camera
        return camera_capture

    def __del__(self):
        try:
            self.current_frame.release()
        except AttributeError:
            pass


if __name__ == '__main__':
    camera = Camera()
    image = camera.capture_image()
    preview_image(image)

    camera = Camera()
    camera.start_capture()
    import cv2

    while True:
        cv2.imshow("Camera Stream", camera.current_frame.read())
        cv2.waitKey(10)
