{
  description = "A tool which generates beautiful nesto-branded qr-codes";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs, poetry2nix }:
    let
      systems = [
        "x86_64-linux"
        "i686-linux"
        "x86_64-darwin"
        "aarch64-linux"
        "armv6l-linux"
        "armv7l-linux"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f system);
    in
    {
      legacyPackages = forAllSystems (system:
        let
          pkgs = import nixpkgs {
            inherit system;
          };
        in
        rec {
          qr-code-generator = pkgs.callPackage ./pkgs { };
          default = qr-code-generator;
        });
      packages = forAllSystems (system: nixpkgs.lib.filterAttrs (_: v: nixpkgs.lib.isDerivation v) self.legacyPackages.${system});
      nixosModules = import ./modules;
    };
}
