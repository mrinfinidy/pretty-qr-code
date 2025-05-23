#!/usr/bin/env python

import qrcode
import qrcode.image.svg
from qrcode.image.styles.moduledrawers.svg import SvgCircleDrawer
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer, RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SolidFillColorMask
import PIL
from PIL import Image, ImageDraw
import os
import sys



#Custom function for eye styling. These create the eye masks
class Qr_img_parts:
    def __init__(self, 
        embeded_image_name,
        inner_eyes_img,
        inner_eye_mask,
        outer_eyes_img,
        outer_eye_mask,
        qr_img,
        qr_img_simple
        ) -> None:
        self.embeded_image_name = embeded_image_name
        self.inner_eyes_img = inner_eyes_img
        self.inner_eye_mask = inner_eye_mask
        self.outer_eyes_img = outer_eyes_img
        self.outer_eye_mask = outer_eye_mask
        self.qr_img = qr_img
        self.qr_img_simple = qr_img_simple

def style_inner_eyes(img):
  img_size = img.size[0]
  eye_size = 70 #default
  quiet_zone = 40 #default
  mask = Image.new('L', img.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((60, 60, 90, 90), fill=255) #top left eye
  draw.rectangle((img_size-90, 60, img_size-60, 90), fill=255) #top right eye
  draw.rectangle((60, img_size-90, 90, img_size-60), fill=255) #bottom left eye
  return mask

def style_outer_eyes(img):
  img_size = img.size[0]
  eye_size = 70 #default
  quiet_zone = 40 #default
  mask = Image.new('L', img.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((40, 40, 110, 110), fill=255) #top left eye
  draw.rectangle((img_size-110, 40, img_size-40, 110), fill=255) #top right eye
  draw.rectangle((40, img_size-110, 110, img_size-40), fill=255) #bottom left eye
  draw.rectangle((60, 60, 90, 90), fill=0) #top left eye
  draw.rectangle((img_size-90, 60, img_size-60, 90), fill=0) #top right eye
  draw.rectangle((60, img_size-90, 90, img_size-60), fill=0) #bottom left eye  
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
def create_img(qr, input_img):
    inner_eyes_img = qr.make_image(
            image_factory=StyledPilImage,
            eye_drawer=RoundedModuleDrawer(),
            color_mask=SolidFillColorMask(front_color=(0, 162, 174))
        )
    
    outer_eyes_img = qr.make_image(
            image_factory=StyledPilImage,
            eye_drawer=RoundedModuleDrawer(),
            color_mask=SolidFillColorMask(front_color=(0, 0, 0))
        )

    embeded_image_name = input_img

    if embeded_image_name == 'pos-adapter':
        embeded_image_path = os.getenv('NESTO_DEFAULT_QR_LOGO_POS_ADAPTER', './assets/nesto-pos-logo.png')
    else:
        embeded_image_path = os.getenv('NESTO_DEFAULT_QR_LOGO', './assets/default.png')

    qr_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=CircleModuleDrawer(),
            embeded_image_path = embeded_image_path
        )
    
    qr_img_simple = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=CircleModuleDrawer()
        )

    inner_eye_mask = style_inner_eyes(qr_img)
    outer_eye_mask = style_outer_eyes(qr_img)
    return Qr_img_parts(embeded_image_name, inner_eyes_img, inner_eye_mask, outer_eyes_img, outer_eye_mask, qr_img, qr_img_simple)

# Generate qr code based on image input
def generate_qr_code(
        qr,
        qr_img_parts
    ):
    qr_img_parts.inner_eyes_img = qr_img_parts.inner_eyes_img.convert("RGBA")
    qr_img_parts.outer_eyes_img = qr_img_parts.outer_eyes_img.convert("RGBA")
    qr_img_parts.qr_img = qr_img_parts.qr_img.convert("RGBA")
    qr_img_parts.inner_eye_mask = qr_img_parts.inner_eye_mask.convert("L")
    qr_img_parts.outer_eye_mask = qr_img_parts.outer_eye_mask.convert("L")
    if not qr_img_parts.embeded_image_name or qr_img_parts.embeded_image_name == 'blank':
        intermediate_img = Image.composite(qr_img_parts.inner_eyes_img, qr_img_parts.qr_img_simple, qr_img_parts.inner_eye_mask)
    elif qr_img_parts.embeded_image_name == 'default' or qr_img_parts.embeded_image_name == 'pos-adapter':
        intermediate_img = Image.composite(qr_img_parts.inner_eyes_img, qr_img_parts.qr_img, qr_img_parts.inner_eye_mask)
    else:
        qr_img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=CircleModuleDrawer(),
                embeded_image_path = os.path.join('./assets/', qr_img_parts.embeded_image_name)
            )
        intermediate_img = Image.composite(qr_img_parts.inner_eyes_img, qr_img, qr_img_parts.inner_eye_mask)

    return Image.composite(qr_img_parts.outer_eyes_img, intermediate_img, qr_img_parts.outer_eye_mask)

# Save the image to a file
def save_img(final_img, output_name):
    result_path = 'result/'
    if not os.path.exists(result_path):
        os.makedirs((result_path))
    if not output_name:
        result_path = os.path.join(result_path, 'qrcode.png')
    else:
        result_path = os.path.join(result_path, output_name + '.png');
    print("Saving to: ", result_path)
    final_img.save(result_path)

# main function that calls all steps needed to make a qrcode
def make_qrcode(input_data, input_image, output_name):
    qr = create_qrcode_instance()
    add_data(qr, input_data)
    qr_img_parts = create_img(qr, input_img)
    final_img = generate_qr_code(qr, qr_img_parts)
    save_img(final_img, output_name)

# Additionaly to the png qrcode an svg is created as well
def make_qrcode_svg(input_data, output_name):
    qr = create_qrcode_instance()
    add_data(qr, input_data)
    qr_svg = qr.make_image(
        image_factory=qrcode.image.svg.SvgImage,
        module_drawer=SvgCircleDrawer(),
    )
    result_path = 'result/'
    if not os.path.exists(result_path):
        os.makedirs((result_path))
    if not output_name:
        result_path = os.path.join(result_path, 'qrcode.svg')
    else:
        result_path = os.path.join(result_path, output_name + '.svg');
    qr_svg.save(result_path)


if len(sys.argv) == 4:
    input_data = sys.argv[1]
    input_img = sys.argv[2]
    output_name = sys.argv[3]
    make_qrcode(input_data, input_img, output_name)
    make_qrcode_svg(input_data, output_name)
elif len(sys.argv) != 1:
    print("Usage: qr-code-generator <data_to_encode> <image_file_name> <output_file_name>")
else:
    input_data = input('1) Input data (url) you want to encode:\n')
    print()
    input_img = input('2) Input file name (e.g. \'xyz.png\') for the center image:\n(leave blank for no image or \'default\' for generic nesto logo or \'pos-adapter\' for pos-adapter logo)\n')
    print()
    output_name = input('3)Input result file name:\n')
    make_qrcode(input_data, input_img, output_name)
    make_qrcode_svg(input_data, output_name)
