#!/usr/bin/env python

import qrcode
from qrcode.image.styles import colormasks
import qrcode.image.svg
from qrcode.image.styles.moduledrawers.svg import SvgCircleDrawer
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer, RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SolidFillColorMask
from PIL import Image, ImageDraw
import os
import sys

#Custom function for eye styling. These create the eye masks
class Qr_image_parts:
    def __init__(self, 
        embeded_image_name,
        inner_eyes_image,
        inner_eye_mask,
        outer_eyes_image,
        outer_eye_mask,
        qr_image,
        qr_image_simple
        ) -> None:
        self.embeded_image_name = embeded_image_name
        self.inner_eyes_image = inner_eyes_image
        self.inner_eye_mask = inner_eye_mask
        self.outer_eyes_image = outer_eyes_image
        self.outer_eye_mask = outer_eye_mask
        self.qr_image = qr_image
        self.qr_image_simple = qr_image_simple

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return (
        int(hex[0:2], 16),
        int(hex[2:4], 16),
        int(hex[4:6], 16),
    )
    

def style_inner_eyes(image):
  image_size = image.size[0]
  eye_size = 70 #default
  quiet_zone = 40 #default
  mask = Image.new('L', image.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((60, 60, 90, 90), fill=255) #top left eye
  draw.rectangle((image_size-90, 60, image_size-60, 90), fill=255) #top right eye
  draw.rectangle((60, image_size-90, 90, image_size-60), fill=255) #bottom left eye
  return mask

def style_outer_eyes(image):
  image_size = image.size[0]
  eye_size = 70 #default
  quiet_zone = 40 #default
  mask = Image.new('L', image.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((40, 40, 110, 110), fill=255) #top left eye
  draw.rectangle((image_size-110, 40, image_size-40, 110), fill=255) #top right eye
  draw.rectangle((40, image_size-110, 110, image_size-40), fill=255) #bottom left eye
  draw.rectangle((60, 60, 90, 90), fill=0) #top left eye
  draw.rectangle((image_size-90, 60, image_size-60, 90), fill=0) #top right eye
  draw.rectangle((60, image_size-90, 90, image_size-60), fill=0) #bottom left eye  
  return mask


# Create a QR code instance
def create_qrcode_instance():
    return qrcode.QRCode(
        version=5,  # QR code version
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Error correction level
        box_size=10,  # Size of each box in the QR code
        border=4,    # Border size
    )

# Add data to the QR code
def add_data(qr, input_data):
    qr.add_data(input_data)
    qr.make(fit=True)

# Create an image from the QR code instance
def create_image(qr, input_image, base_color, inner_eye_color, outer_eye_color):
    inner_eyes_image = qr.make_image(
            image_factory=StyledPilImage,
            eye_drawer=RoundedModuleDrawer(),
            color_mask=SolidFillColorMask(front_color=hex_to_rgb(inner_eye_color))
            #color_mask=SolidFillColorMask(front_color=(0, 162, 174))
        )
    
    outer_eyes_image = qr.make_image(
            image_factory=StyledPilImage,
            eye_drawer=RoundedModuleDrawer(),
            color_mask=SolidFillColorMask(front_color=hex_to_rgb(outer_eye_color))
            # color_mask=SolidFillColorMask(front_color=(0, 0, 0))
        )

    embeded_image_name = input_image

    if embeded_image_name == 'pos-adapter':
        embeded_image_path = os.getenv('NESTO_DEFAULT_QR_LOGO_POS_ADAPTER', './assets/nesto-pos-logo.png')
    else:
        embeded_image_path = os.getenv('NESTO_DEFAULT_QR_LOGO', './assets/default.png')

    qr_image = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=CircleModuleDrawer(),
            color_mask=SolidFillColorMask(front_color=hex_to_rgb(base_color)),
            embeded_image_path = embeded_image_path
        )
    
    qr_image_simple = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=CircleModuleDrawer(),
            color_mask=SolidFillColorMask(front_color=hex_to_rgb(base_color))
            # color_mask=SolidFillColorMask(front_color=(0, 0, 0))
        )

    inner_eye_mask = style_inner_eyes(qr_image)
    outer_eye_mask = style_outer_eyes(qr_image)
    return Qr_image_parts(embeded_image_name, inner_eyes_image, inner_eye_mask, outer_eyes_image, outer_eye_mask, qr_image, qr_image_simple)

# Generate qr code based on image input
def generate_qr_code(
        qr,
        qr_image_parts
    ):
    qr_image_parts.inner_eyes_image = qr_image_parts.inner_eyes_image.convert("RGBA")
    qr_image_parts.outer_eyes_image = qr_image_parts.outer_eyes_image.convert("RGBA")
    qr_image_parts.qr_image = qr_image_parts.qr_image.convert("RGBA")
    qr_image_parts.inner_eye_mask = qr_image_parts.inner_eye_mask.convert("L")
    qr_image_parts.outer_eye_mask = qr_image_parts.outer_eye_mask.convert("L")
    if not qr_image_parts.embeded_image_name or qr_image_parts.embeded_image_name == 'blank':
        intermediate_image = Image.composite(qr_image_parts.inner_eyes_image, qr_image_parts.qr_image_simple, qr_image_parts.inner_eye_mask)
    elif qr_image_parts.embeded_image_name == 'default' or qr_image_parts.embeded_image_name == 'pos-adapter':
        intermediate_image = Image.composite(qr_image_parts.inner_eyes_image, qr_image_parts.qr_image, qr_image_parts.inner_eye_mask)
    else:
        qr_image = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=CircleModuleDrawer(),
                embeded_image_path = os.path.join('./assets/', qr_image_parts.embeded_image_name)
            )
        intermediate_image = Image.composite(qr_image_parts.inner_eyes_image, qr_image, qr_image_parts.inner_eye_mask)

    return Image.composite(qr_image_parts.outer_eyes_image, intermediate_image, qr_image_parts.outer_eye_mask)

# Save the image to a file
def save_image(final_image, output_name):
    result_path = 'result_test/'
    if not os.path.exists(result_path):
        os.makedirs((result_path))
    if not output_name:
        result_path = os.path.join(result_path, 'qrcode.png')
    else:
        result_path = os.path.join(result_path, output_name + '.png');
    print("Saving to: ", result_path)
    final_image.save(result_path)

# main function that calls all steps needed to make a qrcode
def make_qrcode(input_data, input_image, base_color, inner_eye_color, outer_eye_color, output_name):
    qr = create_qrcode_instance()
    add_data(qr, input_data)
    qr_image_parts = create_image(qr, input_image, base_color, inner_eye_color, outer_eye_color)
    final_image = generate_qr_code(qr, qr_image_parts)
    save_image(final_image, output_name)

# Additionaly to the png qrcode an svg is created as well
def make_qrcode_svg(input_data, output_name):
    qr = create_qrcode_instance()
    add_data(qr, input_data)
    qr_svg = qr.make_image(
        image_factory=qrcode.image.svg.SvgImage,
        module_drawer=SvgCircleDrawer(),
    )
    result_path = 'result_test/'
    if not os.path.exists(result_path):
        os.makedirs((result_path))
    if not output_name:
        result_path = os.path.join(result_path, 'qrcode.svg')
    else:
        result_path = os.path.join(result_path, output_name + '.svg');
    qr_svg.save(result_path)


# if len(sys.argv) == 4:
#     input_data = sys.argv[1]
#     input_image = sys.argv[2]
#     output_name = sys.argv[3]
#     make_qrcode(input_data, input_image, output_name)
#     make_qrcode_svg(input_data, output_name)
# elif len(sys.argv) != 1:
#     print("Usage: qr-code-generator <data_to_encode> <image_file_name> <output_file_name>")
# else:
#     input_data = input('1) Input data (url) you want to encode:\n')
#     print()
#     input_image = input('2) Input file name (e.g. \'xyz.png\') for the center image:\n(leave blank for no image or \'default\' for generic nesto logo or \'pos-adapter\' for pos-adapter logo)\n')
#     print()
#     output_name = input('3)Input result file name:\n')
#     make_qrcode(input_data, input_image, output_name)
#     make_qrcode_svg(input_data, output_name)
