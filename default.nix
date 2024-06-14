{pkgs, fetchurl, lib, stdenv, ...}:
with pkgs.python311Packages;
{
  all = buildPythonPackage {
    pname = "crunchyroll";
    version = "2024-06-07";
    src = lib.fileset.toSource {
      root = ./.;
      fileset = ./.;
    };

    format = "other";

    dependencies = [
      pulsectl
      yt-dlp
    ];

    postInstall = ''
      mkdir -p $out/bin
      cp -v bt.py $out/bin/bt
      cp -v crunchyroll $out/bin/crunchyroll
      cp -v change_default_sink $out/bin/change_default_sink
      cp -v headset.py $out/bin/headset
      cp -v renum.py $out/bin/renum
      cp -v video-dl.py $out/bin/video-dl
    '';
  };

  bt = buildPythonPackage {
    pname = "bt";
    version = "2024-06-07";
    src = lib.fileset.toSource {
      root = ./.;
      fileset = ./bt.py;
    };

    format = "other";

    postInstall = ''
      mkdir -p $out/bin
      cp -v bt.py $out/bin/bt
    '';
  };

  change-default = buildPythonPackage {
    pname = "change-default";
    version = "2024-06-07";
    src = lib.fileset.toSource {
      root = ./.;
      fileset = ./change_default_sink;
    };

    format = "other";

    dependencies = [
      pulsectl
    ];

    postInstall = ''
      mkdir -p $out/bin
      cp -v change_default_sink $out/bin/change_default_sink
    '';
  };

  crunchyroll = buildPythonPackage {
    pname = "crunchyroll";
    version = "2024-06-07";
    src = lib.fileset.toSource {
      root = ./.;
      fileset = ./crunchyroll;
    };

    format = "other";

    dependencies = [
      yt-dlp
    ];

    postInstall = ''
      mkdir -p $out/bin
      cp -v crunchyroll $out/bin/crunchyroll
    '';
  };

  headset = buildPythonPackage {
    pname = "headset";
    version = "2024-06-07";
    src = lib.fileset.toSource {
      root = ./.;
      fileset = ./headset.py;
    };

    format = "other";

    postInstall = ''
      mkdir -p $out/bin
      cp -v headset.py $out/bin/headset
    '';
  };

  renum = buildPythonPackage {
    pname = "renum";
    version = "2024-06-07";
    src = lib.fileset.toSource {
      root = ./.;
      fileset = ./renum.py;
    };

    format = "other";

    postInstall = ''
      mkdir -p $out/bin
      cp -v renum.py $out/bin/renum
    '';
  };

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