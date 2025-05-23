{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  nativeBuildInputs = [
    pkgs.python311Packages.qrcode
    pkgs.python311Packages.pillow
  ];
}
