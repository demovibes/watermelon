# watermelon/contrib

This folder contains additional scripts and connectors to help watermelon
communicate with backend services.

There are several methods to set up the stream source that will connect to
Icecast for broadcasting, including:

* IceS
* demosauce
* liquid-soap

## IceS

IceS is the standard "stream client" provided by the Icecast developers.  It
is very simple but the main drawback is that it will only produce .ogg vorbis
output streams, which means that your Icecast server will only broadcast .ogg
vorbis.  For modern browsers and players this works fine, but it prevents you
from offering a different format (.mp3, .m4a/aac, .opus).

Note that just because **output** is in .ogg does not mean **input** must too!
IceS accepts .wav input, and will re-encode to .ogg on the fly.  As long as
there is a player available for your stored files, they can be decoded to .wav
and handed to IceS for broadcast.

IceS can be set up in a few ways:
* If all audio on your site is already in .ogg format, it can be given directly
to IceS for broadcast without re-encoding.  This is the least flexible solution
because the audio cannot be changed (no replaygain, etc) and must already be in
a format that matches the broadcast spec.

    To use this, set your ices.xml to mode "playlist" / "script", and the script
    should retrieve the next song from the db and return its filename.

* Similar to the above: if the site is configured to re-encode and cache song
files, then the preprocessed versions can be given to IceS instead.  However,
the trade-off is that any change to the processing algorithm (new bitrate, new
format, adjust volume etc) needs a re-encode of every song in the database.

* Audio can be re-encoded per song into a compatible .ogg format, then given to
IceS for broadcast.  An example of this might be a script that uses SoX to read
files and produce .ogg.  This allows users to accept a variety of formats and
apply normalization, etc.  However the encoding process can be slow and this
would result in noticeable gaps between playback.

    To use this, set your ices.xml to mode "playlist" / "script", and the script
    should retrieve the next song from the db, re-encode to a temp file, and
    return the temp filename.

* Audio can be decoded per song into a compatible .wav format, and given to the
IceS client via `stdin`.  This is the fastest and most flexible solution, but
is complicated because the script is no longer triggered automatically by a
callback and must instead run continuously in the background to keep the stdin
pipe fed.

    To use this, set ices.xml to mode "playlist" / "StdinPCM".  It is best to
    create a named pipe (using `mkfifo`) to connect the decoder script to the
    IceS input sink.  From here, the script should continually decode the next
    song and pass it to IceS for processing.  Remember that when each song is
    complete, the script should also rewrite the metadata.txt file and send a
    SIGUSR1 to IceS so it can keep metadata updated.

Given that most users do not have a consistent .ogg library, a re-encoding
solution is likely, and so an external decoder program will be necessary.  For
MP3 files this can be mpg123 or mpg321, but for a more general solution, it is
possible to configure SoX or ffmpeg to handle the conversion.

Examples of these setups are found in the IceS folder.

## Demosauce

demosauce is an Icecast-enabled stream client developed for demovibes.  It can
connect directly to an Icecast broadcast server, play back a variety of song
formats, and is controllable via commands sent over a socket.  Its output is
an mp3 stream using liblame.

The main advantages of using demosauce are its support for a variety of exotic
file formats: FLAC, MP3, OGG etc, but also a number of tracker formats using
the OpenMPT library.  It comes with a separate program called `dscan` which
reads a source file and returns information about it: length, bitrate, replay
gain, etc.  This is called by the upload processing to determine if the upload
is valid, and retrieve some playback info that the streamer later uses.

demosauce is available at gitlab from this link:
https://gitlab.com/maep/demosauce

## Liquidsoap

Liquidsoap is a complete framework in Ocaml for building audio streams.

Liquidsoap's strength is its flexibility: the stream pipeline is described in
config files, allowing definition of source to sink with processing stages
between.  Multiple sources can be combined into a sink, with failover support,
and custom manipulation of audio in between (e.g. LADSPA plugins or similar).

Input plugins include FLAC, AAC, OGG, MP3, speex, opus, and many more.  Several
output stream formats are also available, including two flavors of MP3, AAC,
OPUS, etc.  It is even possible to use one source with multiple encoders, to
stream the same content in different formats and/or bitrates.

The drawback is its complexity in defining the pipeline.  A sample liquidsoap
flow is provided, but more complicated setups will require reading the manual
and adjusting accordingly.

The liquidsoap project is available here: https://www.liquidsoap.info/
