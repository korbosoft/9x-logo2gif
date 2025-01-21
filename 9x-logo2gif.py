#!/usr/bin/env python3

import argparse
import os
import sys
from PIL import Image

def cycle(im: Image, paloffset: int, amount: int):
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
        pal = pal[:paloffset] + pal[paloffset-255:] + list(zip(*[iter(pal[paloffset])]*3))
    return [item for t in pal for item in t]
def main():
    frames = []

    parser = argparse.ArgumentParser(prog='9x-logo2gif',
                                     description='Generates an animated GIF from a Windows 9x LOGO.SYS file', usage='%(prog)s [-h] input [-o OUTPUT]')
    parser.add_argument('input',
        help='Path to a LOGO.SYS-type file',
        )
    parser.add_argument('-o', '--output',
        help='Path to output GIF',
        default='logo.gif'
        )

    args = parser.parse_args()
    with Image.open(args.input) as logo:
        with open(args.input, 'rb') as f:
            f.seek(0x32)
            paloffset = int.from_bytes(f.read(1))
            print(paloffset)
        logo = logo.resize([640, 400])
        for i in range(paloffset):
            with logo.copy() as frame:
                frame.putpalette(cycle(frame, paloffset, i))
                frames.append(frame)
        frames[0].save(args.output,
                       'GIF', save_all=True, append_images=frames[1:], duration=100, loop=0)
        print(f'Saved to {args.output}')

if __name__ == '__main__':
    main()
