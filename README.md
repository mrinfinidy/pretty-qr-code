# Nesto QR-Code Generator

## Description
This project emerged from the needs of the pos-adapter team to create beautiful qr-codes for marketing material and manuals.
You can use it to embed URLs. Optionally, you can place a logo in the center of the code.
The resulting image adheres to the Nesto corporate branding guidelines in terms of color schemas.

## Install 

### NixOS
This tool is packaged as a NixOS package. You might want to install it using the following flake input:

```
qr-code-generator = {
    url = "git+https://_:<access-token>@gitlab.nesto.app/nesto-software/pos-adapter-v2/qr-code-generator?ref=main";
    inputs.nixpkgs.follows = "nixpkgs";
};
```

Further, add the following to your home-manager config:

```
home-manager.users.<your-user> = {
    home.packages = [
        (qr-code-generator.packages.${system}.default.override
        {
            inherit pkgs;
        })
    ];
};
```

You might also want to add:

```
nixpkgs.config.allowUnfreePredicate = pkg: builtins.elem (lib.getName pkg) [
    "qr-code-generator"
];
```

### Manual
#### Requirements
- Python 3
- pip
    - qrcode
    - Pillow

#### Install Dependencies
You can install the pip packages directly on your system or in a virtual environment.
1) `python -m venv qrenv` (only if you run the tool in a virtual environment)
2) `source qrenv/bin/activate` (only if you run the tool in a virtual environment)
3) `pip install qrcode`
4) `pip install Pillow`

## Usage

### NixOS
If you installed the package into your PATH with the methods listed above, you can just run: `qr-code-generator`
### Manual Installation
Launch script from project root directory:
`python ./qr-code-generator`

If you don't pass any command line arguments an interactive version of this tool will run.\
You can also run the script with the following arguments:\
`python ./qr-code-generator <data_to_encode> <image_file_name> <output_file_name>`

Pass `default` as image_file_name in order to use the standard Nesto logo.\
Pass `""` or `blank` as image_file_name if you don't want to use an image.\
You can store an image in the assets folder and pass the file name if you want to use you own image.

### Sample Command
`./result/bin/entrypoint.py --data "https://github.com/mrinfinidy/qr-code-generator/tree/develop" --input default --style circle --style-inner round --style-outer round --base "#222433" --color-inner "#737BAB" --color-outer "#ff7373" --output "/home/bignixy/Pictures/" --svg`

## TODOs

- Pass inputs as cli args instead of interactive prompt (&check;)
- Write a proper usage section for manual installation (&check;)
- Add top padding to pos-adapter-logo.png
