#!/usr/bin/env python

import sys, getopt
from qr_code_generator import make_qrcode, make_qrcode_svg

def print_usage():
    print("""Usage: entrypoint.py [options]

Options:
  -h, --help            Show this help message and exit
  -d, --data            Data to encode in QR code (required)
  -i, --input           Input image file (optional)
  -b, --base            Base color hex code (e.g. #000000)
  -n, --inner           Inner eye color hex code
  -r, --outer           Outer eye color hex code
  -o, --output          Output file name (required)
  -s, --svg             Also generate SVG output (flag, optional)

Example:
  entrypoint.py -d "https://example.com" -i logo.png -b #000000 -n #000fff -r #fff000 -o qrcode.png -s
""")

def main (argv):
    print("Arguments: ", argv)
    input_data = ''
    input_image = ''
    base_color = ''
    inner_eye_color = ''
    outer_eye_color = ''
    include_svg = False
    output_name = ''
    
    try:
        opts, args = getopt.getopt(argv, "hi:o:d:b:n:r:s", ["input=", "output=", "data=", "base=", "inner=", "outer=", "svg"])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    print("Parsed options: ", opts)
    for opt, arg in opts:
        if opt == '-h':
            print('entrypoint.py -i <input_image> -o <output_name> -d <data_to_encode>')
            sys.exit()
        elif opt in ("-d", "--data"):
            input_data = arg
        elif opt in ("-i", "--input"):   # lowercase i for input, to match getopt
            input_image = arg
        elif opt in ("-b", "--base"):
            base_color = arg
        elif opt in ("-n", "--inner"):
            inner_eye_color = arg
        elif opt in ("-r", "--outer"):
            outer_eye_color = arg
        elif opt in ("-s", "--svg"):
            include_svg = True
        elif opt in ("-o", "--output"):
            output_name = arg
    make_qrcode(input_data, input_image, base_color, inner_eye_color, outer_eye_color, output_name)
    if include_svg:
        make_qrcode_svg(input_data, output_name)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
