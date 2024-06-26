{pkgs, fetchurl, lib, stdenv, ...}:
with pkgs.python311Packages;
{
  bluetooth = buildPythonPackage {
    pname = "bluetooth";
    version = "2024-06-14";
    src = ./bluetooth;

    format = "other";

    postInstall = ''
      mkdir -p $out/bin
      cp -v bluetooth $out/bin/bluetooth
    '';
  };
  disk = buildPythonPackage {
    pname = "disk";
    version = "2024-06-14";
    src = ./disk;

    format = "other";

    dependencies = [
      psutil
    ];

    postInstall = ''
      mkdir -p $out/bin
      cp -v disk $out/bin/disk
    '';
  };
  network = buildPythonPackage {
    pname = "network";
    version = "2024-06-16";
    src = ./network;

    format = "other";

    dependencies = [
      psutil
    ];

    postInstall = ''
      mkdir -p $out/bin
      cp -v network $out/bin/network
    '';
  };
  video-dl = buildPythonPackage {
    pname = "video-dl";
    version = "2024-06-26";
    src = ./video-dl;

    format = "other";

    dependencies = [
      yt-dlp
    ];

    postInstall = ''
      mkdir -p $out/bin
      cp -v video-dl.py $out/bin/video-dl
      cp -v video-dl.py $out/bin/music-dl
    '';
  };
  volume = buildPythonPackage {
    pname = "volume";
    version = "2024-06-14";
    src = ./volume;

    format = "other";

    dependencies = [
      yt-dlp
    ];

    postInstall = ''
      mkdir -p $out/bin
      cp -v volume $out/bin/volume
    '';
  };
  weather = buildPythonPackage {
    pname = "weather";
    version = "2024-06-16";
    src = ./weather;

    format = "other";

    dependencies = [
      geopy
      (
        buildPythonPackage rec {
          pname = "suntime";
          version = "1.3.2";
          src = fetchPypi {
            inherit pname version;
            sha256 = "sha256-SDT3kHrRPbs2mQTLX0N27cCwbG6KHPwKrBJo9k0Ozc8=";
          };
          doCheck = false;
        }
      )
      requests
      tzlocal
    ];

    postInstall = ''
      mkdir -p $out/bin
      cp -v weather $out/bin/weather
    '';
  };
  workspaces = buildPythonPackage {
    pname = "workspaces";
    version = "2024-06-14";
    src = ./workspaces;

    format = "other";

    postInstall = ''
      mkdir -p $out/bin
      cp -v workspaces $out/bin/workspaces
    '';
  };
}