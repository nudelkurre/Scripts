{
  description = "Flake to import scripts into nixos";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
      scripts = import ./. { inherit (pkgs) pkgs buildPythonPackage fetchurl lib stdenv; };
    in {
      packages = 
        scripts;

      apps.${system} = {
        video-dl = {
          type = "app";
          program = "${self.packages.video-dl}/bin/video-dl";
        };
      };
    });
}