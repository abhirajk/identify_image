import signal
import sys

from raspi_utils.CameraPlatform import CameraPlatform

cameraPlatform = CameraPlatform();


def sigint_handler(sig, frame):
    cameraPlatform.clean();
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def main(args: list[str]) -> None:
    try:
        cameraPlatform.scanXPlane();
        cameraPlatform.clean();
    finally:
        print("Done Scanning")


if __name__ == '__main__':
    main(sys.argv[1:])
