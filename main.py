# main.py — Hello World on Waveshare 2.66" e-paper (portrait)

import utime
from epd_2in66 import EPD_2in66

def main():
    epd = EPD_2in66()      # __init__ already calls init(0) for you

    # Draw into the portrait framebuffer
    epd.image_Landscape.fill(0xFF)     # white background
    epd.image_Landscape.text("Hello, world!", 12, 64, 0x00)  # black text

    # Send that framebuffer to the display
    epd.display_Landscape(epd.buffer_Landscape)

    utime.sleep_ms(2000)
    epd.sleep()

if __name__ == "__main__":
    main()