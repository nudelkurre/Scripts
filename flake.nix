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
        bluetooth = {
          type = "app";
          program = "${self.packages.bluetooth}/bin/bluetooth";
        };
        disk = {
          type = "app";
          program = "${self.packages.disk}/bin/disk";
        };
        network = {
          type = "app";
          program = "${self.packages.network}/bin/network";
        };
        video-dl = {
          type = "app";
          program = "${self.packages.video-dl}/bin/video-dl";
        };
        volume = {
          type = "app";
          program = "${self.packages.volume}/bin/volume";
        };
        weather = {
          type = "app";
          program = "${self.packages.weather}/bin/weather";
        };
        workspaces = {
          type = "app";
          program = "${self.packages.workspaces}/bin/workspaces";
        };
      };
    });
}
