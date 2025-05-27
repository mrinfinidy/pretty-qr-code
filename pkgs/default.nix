{ lib, pkgs, ... }:

pkgs.python3Packages.buildPythonApplication {
  pname = "qrcode-pretty";
  version = "1.0.0";
  src = ./..;
  doCheck = false;

  nativeBuildInputs = [
    pkgs.python3Packages.setuptools
  ];

  propagatedBuildInputs = [
    pkgs.python3Packages.qrcode
    pkgs.python3Packages.pillow
  ];

  makeWrapperArgs = [
    "--set DEFAULT_IMAGE ${./../assets/default.png}"
  ];

  meta = with lib; {
    homepage = "https://github.com/mrinfinidy/pretty-qr-code";
    description = "A tool which generates beautiful QR codes with customizable styles and embedded images";
    license = licenses.unfree;
  };
}
