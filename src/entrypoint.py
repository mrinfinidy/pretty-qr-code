#!/usr/bin/env python

import sys, getopt, os
from qr_code_generator import make_qrcode, make_qrcode_svg
from const import ( DRAWER_CLASSES, ERROR_CORRECTION_LEVELS )

def print_usage():
    print("""Usage: entrypoint.py [options]

Options:
  -h, --help                  Show this help message and exit
  -d, --data <data>           Data to encode in QR code (required)
  -i, --input <image>         Input image file name (optional)
  -s, --style <style>         Style for the QR code modules (optional)
      --style-inner <style>   Style for the inner eyes (optional)
      --style-outer <style>   Style for the outer eyes (optional)
  -b, --base <hex>            Base color hex code (e.g. #000000)
  -n, --color-inner <hex>     Inner eye color hex code
  -r, --color-outer <hex>     Outer eye color hex code
  -o, --output <dir>          Output directory path (default: ./qrcode-output/)
      --svg                   Also generate SVG output (optional flag)
      --version <int>         QR version (default: 5)
      --box-size <int>        Box size in pixels (default: 10)
      --border <int>          Border size in boxes (default: 4)
      --error-correction <L|M|Q|H>  Error correction level (default: H)

Available styles: square, gapped-square, circle, round, vertical-bars, horizontal-bars

Example:
  entrypoint.py -d "https://example.com" -i logo.png -b #000000 -n #000fff -r #fff000 -o ./output --style circle --style-inner square --style-outer circle --svg
""")

def main (argv):
    input_data = ''
    input_image = ''
    drawer_instance = DRAWER_CLASSES['square']()
    drawer_instance_inner = DRAWER_CLASSES['square']()
    drawer_instance_outer = DRAWER_CLASSES['square']()
    base_color = '#000000'
    inner_eye_color = '#000000'
    outer_eye_color = '#000000'
    include_svg = False
    version = 5
    error_correction = ERROR_CORRECTION_LEVELS['H']
    box_size = 10
    border = 4
    output_dir = './qrcode-output/'
    
    try:
        opts, args = getopt.getopt(
            argv,
            "hi:o:d:b:n:r:",
            [
            "input=",
                "output=",
                "data=",
                "base=",
                "color-inner=",
                "color-outer=",
                "svg",
                "style=",
                "style-inner=",
                "style-outer=",
                "version=",
                "box-size=",
                "border=",
                "error-correction="
            ]
        )
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-d", "--data"):
            input_data = arg
        elif opt in ("-i", "--input"):   # lowercase i for input, to match getopt
            input_image = arg
        elif opt in ("-s", "--style"):
            style = arg
            if style not in DRAWER_CLASSES:
                print(f"Error: style '{style}' not recognized. Choose one of: {', '.join(DRAWER_CLASSES.keys())}")
                sys.exit(1)
            drawer_instance = DRAWER_CLASSES[style]()
        elif opt == "--style-inner":
            style_inner = arg
            if style_inner not in DRAWER_CLASSES:
                print(f"Error: style-inner '{style_inner}' not recognized. Choose one of: {', '.join(DRAWER_CLASSES.keys())}")
                sys.exit(1)
            drawer_instance_inner = DRAWER_CLASSES[style_inner]()
        elif opt == "--style-outer":
            style_outer = arg
            if style_outer not in DRAWER_CLASSES:
                print(f"Error: style-outer '{style_outer}' not recognized. Choose one of: {', '.join(DRAWER_CLASSES.keys())}")
                sys.exit(1)
            drawer_instance_outer = DRAWER_CLASSES[style_outer]()
        elif opt in ("-b", "--base"):
            base_color = arg
        elif opt in ("-n", "--color-inner"):
            inner_eye_color = arg
        elif opt in ("-r", "--color-outer"):
            outer_eye_color = arg

        elif opt == "--version":
            version = int(arg)
        elif opt == "--box-size":
            box_size = int(arg)
        elif opt == "--border":
            border = int(arg)
        elif opt == "--error-correction":
            ec_levels = {
                'L': ERROR_CORRECTION_LEVELS['L'],
                'M': ERROR_CORRECTION_LEVELS['M'],
                'Q': ERROR_CORRECTION_LEVELS['Q'],
                'H': ERROR_CORRECTION_LEVELS['H']
            }
            if arg.upper() in ec_levels:
                error_correction = ec_levels[arg.upper()]
            else:
                print("Invalid error correction level. Choose from: L, M, Q, H.")
                sys.exit(1)
        elif opt == "--svg":
            include_svg = True
        elif opt in ("-o", "--output"):
            output_dir = arg

    make_qrcode(
        input_data,
        input_image,
        drawer_instance,
        drawer_instance_inner,
        drawer_instance_outer,
        base_color,
        inner_eye_color,
        outer_eye_color,
        version,
        error_correction,
        box_size,
        border,
        output_dir
    )
    if include_svg:
        make_qrcode_svg(input_data, output_dir)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
