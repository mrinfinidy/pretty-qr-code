#!/usr/bin/env python

import qrcode
import sys

data_to_encode = sys.argv[1]

qr = qrcode.QRCode(
    version=5,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(data_to_encode)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("qr_simple.png")
