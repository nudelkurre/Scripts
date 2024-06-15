{pkgs, fetchurl, lib, stdenv, ...}:
with pkgs.python311Packages;
{
  video-dl = buildPythonPackage {
    pname = "video-dl";
    version = "2024-06-14";
    src = lib.fileset.toSource {
      root = ./.;
      fileset = ./video-dl.py;
    };

    format = "other";

    dependencies = [
      yt-dlp
    ];

    postInstall = ''
      mkdir -p $out/bin
      cp -v video-dl.py $out/bin/video-dl
      ln -s $out/bin/video-dl $out/bin/music-dl
    '';
  };
}