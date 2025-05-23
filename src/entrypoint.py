import sys, getopt
from qr_code_generator import make_qrcode, make_qrcode_svg

def main (argv):
    input_data = ''
    input_image = ''
    base_color = ''
    inner_eye_color = ''
    outer_eye_color = ''
    include_svg = False
    output_name = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:d:", ["input=", "output=", "data="])
    except getopt.GetoptError:
        print('entrypoint.py -i <input_image> -o <output_name> -d <data_to_encode>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('entrypoint.py -i <input_image> -o <output_name> -d <data_to_encode>')
            sys.exit()
        elif opt in ("-d", "--data"):
            input_data = arg
        elif opt in ("-i", "--input"):
            input_image = arg
        elif opt in ("-b", "--base"):
            base_color = arg
        elif opt in ("-i", "--inner"):
            inner_eye_color = arg
        elif opt in ("-o", "--outer"):
            outer_eye_color = arg
        elif opt in ("-s", "--svg"):
            include_svg = True
        elif opt in ("-o", "--output"):
            output_name = arg
    make_qrcode()
    if include_svg:
        make_qrcode_svg()
