{ lib, pkgs, ... }:

pkgs.python3Packages.buildPythonApplication {
  pname = "qr-code-generator";
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
    "--set NESTO_DEFAULT_QR_LOGO ${./../assets/default.png}"
    "--set NESTO_DEFAULT_QR_LOGO_POS_ADAPTER ${./../assets/nesto-pos-logo.png}"
  ];

  meta = with lib; {
    homepage = "https://gitlab.nesto.app/nesto-software/pos-adapter-v2/qr-code-generator";
    description = "A tool which generates beautiful nesto-branded qr-codes";
    license = licenses.unfree;
  };
}
