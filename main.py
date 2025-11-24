# main.py — ZEC price ticker on Waveshare 2.66" e-paper (landscape)

import utime
import time
import network
import framebuf

from epd_2in66 import EPD_2in66
from secrets import WIFI_SSID, WIFI_PASSWORD

try:
    import urequests as requests
except ImportError:
    import requests  # if you copied a plain "urequests.py" as "requests.py"


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.2)
    print("Connected:", wlan.ifconfig())
    return wlan


def get_zec_price_usd():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=zcash&vs_currencies=usd"
    resp = requests.get(url)
    data = resp.json()
    resp.close()
    return float(data["zcash"]["usd"])


def draw_big_text(dest_fb, text, x, y, scale=3, color=0):
    char_w = 8
    char_h = 8
    text_w = char_w * len(text)
    text_h = char_h

    buf = bytearray(text_w * text_h // 8)
    tmp = framebuf.FrameBuffer(buf, text_w, text_h, framebuf.MONO_HLSB)

    tmp.fill(1)
    tmp.text(text, 0, 0, 0)

    for j in range(text_h):
        for i in range(text_w):
            px = tmp.pixel(i, j)
            for dy in range(scale):
                for dx in range(scale):
                    dest_fb.pixel(x + i * scale + dx, y + j * scale + dy, px if color == 0 else 1 - px)


def draw_price_screen(epd, price_str, status="OK"):
    fb = epd.image_Landscape

    # full white background in RAM (no hardware clear)
    fb.fill(0xFF)

    # header
    fb.text("ZEC / USD", 10, 10, 0x00)

    # big price
    scale = 3
    y = (152 - 8 * scale) // 2
    x = 10
    draw_big_text(fb, price_str, x, y, scale=scale, color=0)

    # footer status
    fb.text(status, 10, 152 - 16, 0x00)

    epd.display_Landscape(epd.buffer_Landscape)


def loop():
    # init once
    epd = EPD_2in66()
    epd.Clear(0xFF)           # one full-panel clean at startup

    connect_wifi()

    last_price = None
    while True:
        try:
            price = get_zec_price_usd()
            price_str = f"{price:.2f}"
            status = "OK"
        except Exception as e:
            print("Error fetching price:", e)
            price_str = "ERR"
            status = "NET ERR"

        # Optional: only refresh if changed
        if price_str != last_price or status != "OK":
            draw_price_screen(epd, price_str, status=status)
            last_price = price_str

        utime.sleep_ms(60000) # refresh every 60 seconds


if __name__ == "__main__":
    loop()