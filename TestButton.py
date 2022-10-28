from RPi import GPIO

from raspi_utils.Button import Button
import signal
import sys

def sigint_handler(sig, frame):
    GPIO.cleanup();
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)

def handleButton(channel, pin):
    print("State: ", GPIO.input(channel), " / Pin: ", pin);

def main(args: list[str]) -> None:
    for pin in args:
        Button(int(pin), callback=lambda channel: handleButton(channel, pin));
    while True:
        pass

if __name__ == '__main__':
    main(sys.argv[1:])