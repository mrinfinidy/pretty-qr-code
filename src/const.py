from qr_code_generator import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer
)

ALLOWED_STYLES = {
    "SquareModuleDrawer",
    "GappedSquareModuleDrawer",
    "CircleModuleDrawer",
    "RoundedModuleDrawer",
    "VerticalBarsDrawer",
    "HorizontalBarsDrawer"
}

DRAWER_CLASSES = {
    "SquareModuleDrawer": SquareModuleDrawer,
    "GappedSquareModuleDrawer": GappedSquareModuleDrawer,
    "CircleModuleDrawer": CircleModuleDrawer,
    "RoundedModuleDrawer": RoundedModuleDrawer,
    "VerticalBarsDrawer": VerticalBarsDrawer,
    "HorizontalBarsDrawer": HorizontalBarsDrawer,
}

