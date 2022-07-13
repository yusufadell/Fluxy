from utils import is_raspberry_pi

PORT = '5555'
SERVER_ADDRESS = 'localhost'
SOCKET = f"tcp://{SERVER_ADDRESS}:{PORT}"


CAMERA_PORT = 0

IS_RASPBERRY_PI = is_raspberry_pi()
RESOLUTION_H = 320
RESOLUTION_W = 320

GPIO_SWITCH = 24
