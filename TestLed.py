from raspi_utils.Led import Led
import sys

# Setup LED
leds = [Led(19), Led(20), Led(16), Led(12)];
def main(args: list[str]) -> None:
    for led in leds:
        led.blink(2);

if __name__ == '__main__':
    main(sys.argv[1:])
