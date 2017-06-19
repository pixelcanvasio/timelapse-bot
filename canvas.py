#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2
from PIL import Image

colors = [
	(255, 255, 255),
	(228, 228, 228),
	(136, 136, 136),
	(34, 34, 34),
	(255, 167, 209),
	(229, 0, 0),
	(229, 149, 0),
	(160, 106, 66),
	(229, 217, 0),
	(148, 224, 68),
	(2, 190, 1),
	(0, 211, 221),
	(0, 131, 199),
	(0, 0, 234),
	(207, 110, 228),
	(130, 0, 128),
]

BLOCK_SIZE = 64
RADIUS = 7
BLOCKS = 5
SIZE = BLOCKS * (BLOCK_SIZE * RADIUS + BLOCK_SIZE + BLOCK_SIZE * RADIUS)
OFFSET = (SIZE - BLOCK_SIZE) / 2


def fetch():
    try:
        img = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))
        pix = img.load()
        for center_x in [-30, -15, 0, 15, 30]:
            for center_y in [-30, -15, 0, 15, 30]:
                bmp_filename = str(center_x) + "." + str(center_y) + ".bmp"
                print "Downloading", bmp_filename
                request = urllib2.Request(
                    "http://pixelcanvas.io/api/bigchunk/" + bmp_filename,
                    None,
                    {'User-agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'}
                    )
                remote_bmp = urllib2.urlopen(request)
                raw_data = remote_bmp.read()#.ljust(460800,"\0")
                current_byte = 0
                for bigchunk_y in range(center_y-RADIUS,center_y+RADIUS+1):
                    for bigchunk_x in range(center_x-RADIUS,center_x+RADIUS+1):
                        for block_y in range(BLOCK_SIZE):
                            current_y = bigchunk_y * BLOCK_SIZE + block_y
                            for block_x in range(0,BLOCK_SIZE,2):
                                current_x = bigchunk_x * BLOCK_SIZE + block_x
                                pix[current_x + OFFSET, current_y + OFFSET] = colors[ord(raw_data[current_byte]) >> 4]
                                pix[current_x+1  + OFFSET, current_y + OFFSET] = colors[ord(raw_data[current_byte]) & 0x0F]
                                current_byte += 1
        print "Canvas successfully downloaded!"
        return img
    except Exception:
        print "Error downloading canvas!"
        raise
