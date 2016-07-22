# mp3rg (vtuner)

http://mp3rg.furytek.org/

# About

vtuner is a web app that uses low-level C-wrapper Python modules to work with the internals of mp3 files. It uses GStreamer to calculate the appropriate ReplayGain value for mp3 files and Mutagen to read and write to them.

ReplayGain allows music players to normalize loudness for individual tracks or albums. 

ReplayGain is supported in a large number of media players and portable media players/digital audio players. It is loosely based on the Python package <a href="https://pypi.python.org/pypi/rgain>rgain</a>, however the features of vtuner are minimal (only for single mp3 files) to demonstrate it as a web app.
