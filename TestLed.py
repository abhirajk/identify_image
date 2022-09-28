from raspi_utils.Led import Led
import sys

# Setup LED
leds = [Led(23), Led(13), Led(19), Led(26)];
def main(args: list[str]) -> None:
    for led in leds:
        led.blink(2);

if __name__ == '__main__':
    main(sys.argv[1:])
