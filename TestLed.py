from raspi_utils.Led import Led
import sys

def main(args: list[str]) -> None:
    for pin in args:
        Led(int(pin)).blink(2);

if __name__ == '__main__':
    main(sys.argv[1:])
