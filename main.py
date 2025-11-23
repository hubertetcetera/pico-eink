# main.py — Big (~32px) text on Waveshare 2.66" e-paper (landscape)

import utime
from epd_2in66 import EPD_2in66
import framebuf


def draw_big_text(dest_fb, text, x, y, scale=3, color=0):
    """
    Draw 'text' onto dest_fb at (x, y) scaled up by 'scale'.
    Uses a tiny intermediate 8px font framebuffer and scales pixels.
    scale=4 → ~32px height.
    """
    # Built-in font is 8px tall, 8px wide per character
    char_w = 8
    char_h = 8
    text_w = char_w * len(text)
    text_h = char_h

    # Temporary framebuffer for the small text
    buf = bytearray(text_w * text_h // 8)
    tmp = framebuf.FrameBuffer(buf, text_w, text_h, framebuf.MONO_HLSB)

    # Clear temp buffer to white (1)
    tmp.fill(1)
    # Draw normal-size text at (0, 0), black = 0
    tmp.text(text, 0, 0, 0)

    # Scale up onto the destination framebuffer
    for j in range(text_h):
        for i in range(text_w):
            px = tmp.pixel(i, j)
            # px == 0 → black, 1 → white
            for dy in range(scale):
                for dx in range(scale):
                    dest_fb.pixel(x + i * scale + dx, y + j * scale + dy, px if color == 0 else 1 - px)


def main():
    epd = EPD_2in66()   # __init__ already calls init(0)

    # Clear panel to white
    epd.Clear(0xFF)

    # Use the built-in landscape framebuffer
    fb = epd.image_Landscape

    # White background
    fb.fill(0xFF)

    # Roughly center vertically: height is 152, text will be ~32px tall
    scale = 3
    text = "HELLO, WORLD"
    y = (152 - 8 * scale) // 2  # 8px font * scale
    x = 4                      # some left margin

    draw_big_text(fb, text, x, y, scale=scale, color=0)  # black text

    # Push to display using the landscape path
    epd.display_Landscape(epd.buffer_Landscape)

    utime.sleep_ms(2000)
    epd.sleep()


if __name__ == "__main__":
    main()