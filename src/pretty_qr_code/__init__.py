"""Pretty QR Code - Generate beautiful, customizable QR codes."""

__version__ = "1.0.0"

from .qr_code_generator import make_qrcode, make_qrcode_svg
from .const import DRAWER_CLASSES, ERROR_CORRECTION_LEVELS

__all__ = [
    "make_qrcode",
    "make_qrcode_svg",
    "DRAWER_CLASSES",
    "ERROR_CORRECTION_LEVELS",
]
