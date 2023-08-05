CM2C
====
Convert Movie To Cast (CM2C) is a Python application to convert a lot of video files with subtitle(s) to videos supported by Google Chromecast.

Movie extension supported are : mp4, mkv, m4v, avi, mov, mpegts, 3gp, webm, mpg, mpeg, wmv, ogv.

Git project
-----------
https://gitlab.com/ArnaudM/CM2C

Creator
-------
Arnaud Moura (arnaudmoura@gmail.com).

How it works
------------
CM2C analize if the video must be converted to work with a Google Chromecast otherwise it convert the video in MP4 format with only one audio track and no subtitle track. By default, if there are several audio tracks, the english version is keeped.

If there is subtitle, you can burn subtitle into the video or only extract subtitle into SRT/ASS file. By default, if there are several subtitle tracks, the french version is extracted or burned because I'm french :).

Python compatibility
--------------------
Python version 2.7 and newer.

Dependencies
------------
FFmpeg version 3.0.1 and newer (https://ffmpeg.org/).

progressbar2 version 3.12.0 and newer (https://pypi.python.org/pypi/progressbar2/3.12.0).

Install FFmpeg on Windows
~~~~~~~~~~~~~~~~~~~~~~~~~
To install FFmpeg on Windows you must download binaries here : https://ffmpeg.zeranoe.com/builds/.

After you must add the FFmpeg binary folder path in the PATH environment variable.

Install FFmpeg on Mac
~~~~~~~~~~~~~~~~~~~~~~~~~
To install FFmpeg on Mac you must download binaries here : http://www.ffmpegmac.net/.

After you must add the FFmpeg binary folder path in the PATH environment variable.

Install FFmpeg on Linux
~~~~~~~~~~~~~~~~~~~~~~~
Debian, Ubuntu run:
::

 sudo apt-get install ffmpeg

Red Hat, Fedora run:
::

 sudo yum install ffmpeg

Install CM2C
------------
Run the following command in your terminal:
::

 pip install cm2c

Usage
-----
Help text:
::

    Usage: cm2c.py folder [options]
       cm2c.py --file video [options]
       Video extension supported : .mp4, .mkv, .m4v, .avi, .mov, .mpegts, .3gp, .webm, .mpg, .mpeg, .wmv, .ogv

    Options:
      -h, --help            show this help message and exit
      -v, --version         show version
      -f FILE, --file=FILE  video file path
      --force               convert the video(s) even if it already has the right
                            format
      -o, --overwrite       overwrite the converted files
      -n, --no_sub          no subtitle extracted and burn in video
      -b, --burn_sub        burn subtitle in the video
      --extract_all_sub     extract all subtitle and the option --burn_sub is
                            disable
      -e, --ext_sub         use external subtitle in SRT or ASS format to burn it in video, it must have the
                            same name of the video
      -s, --shutdown        shutdown after all conversions (Windows only)
      -p PRESET_NAME, --preset=PRESET_NAME
                            define the preset to convert the video(s) [ultrafast,
                            superfast, veryfast, faster, fast, medium, slow,
                            slower, veryslow] (default superfast). A slower preset
                            will provide better compression (compression is
                            quality per filesize).
      -a audio_name, --audio_language=audio_name
                            define the audio language (default eng)
      -l sub_lang, --sub_language=sub_lang
                            define the sub language (default fre, fr, und)
      -d sub_name, --sub_name_regex=sub_name
                            define the sub name by regex
      -r reg_ex, --regex=reg_ex
                            define regular expression apply on file names during
                            file parsing (python regex format)



