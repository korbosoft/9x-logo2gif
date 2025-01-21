#!/usr/bin/env python3

import argparse
import os
import sys
from PIL import Image

def cycle(im: Image, amount: int):
    pal = list(zip(*[iter(im.getpalette())]*3))
    if pal is None:
        raise TypeError("Tried to get color palette, but got None instead. Length is probably over 256.")
    elif len(pal) != 256:
        raise IndexError("Logo does not have 256 colors.")
    # print(pal)
    # print(2)
    # print(pal[:236] + pal[-19:] + list(zip(*[iter(pal[236])]*3)))
    # print(list(iter(iter(pal))))
    for i in range(amount):
        pal = pal[:236] + pal[-19:] + list(zip(*[iter(pal[236])]*3))
    return [item for t in pal for item in t]
def main():
    frames = []

    parser = argparse.ArgumentParser(prog='9x-logo2gif',
                                     description='Generates an animated GIF from a Windows 9x LOGO.SYS file')

    parser.add_argument('filename',
        help='Path to a LOGO.SYS-type file',
        )

    args = parser.parse_args()

    with Image.open(args.filename) as logo:
        logo = logo.resize([640, 400])
        for i in range(20):
            with logo.copy() as frame:
                frame.putpalette(cycle(frame, i))
                frames.append(frame)
        frames[0].save('logo.gif',
                       save_all=True, append_images=frames[1:], duration=100, loop=0)

if __name__ == '__main__':
    main()
