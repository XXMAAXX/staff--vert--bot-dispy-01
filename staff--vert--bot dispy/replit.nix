{ pkgs }: {
  deps = [
    pkgs.libopus
    pkgs.jellyfin-ffmpeg.bin
    pkgs.ffmpeg
  ];
}