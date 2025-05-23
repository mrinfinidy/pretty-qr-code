#!/usr/bin/env python

from qr_code_generator import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer
)

ALLOWED_STYLES = {
    "square",
    "gapped-square",
    "circle",
    "round",
    "vertical-bars",
    "horizontal-bars"
}

DRAWER_CLASSES = {
    "square": SquareModuleDrawer,
    "gapped-square": GappedSquareModuleDrawer,
    "circle": CircleModuleDrawer,
    "round": RoundedModuleDrawer,
    "vertical-bars": VerticalBarsDrawer,
    "horizontal-bars": HorizontalBarsDrawer,
}

