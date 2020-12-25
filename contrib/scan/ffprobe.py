#!/usr/bin/env python

"""
ffprobe scan connector for watermelon

Given a filename on command line, calls ffprobe, and returns key-value data for
insert into the DB.
"""

from ffmpeg import probe


def scan(filepath):
    probe_dict = probe(filepath)

    # perform some validation
    audio_stream = None
    for stream in probe_dict['streams']:
        if stream['codec_type'] == 'audio':
            if audio_stream is None:
                audio_stream = stream
            else:
                raise ValueError("'{0}' is not a supported audio file: multiple audio streams detected".format(filepath))

    if audio_stream is None:
        raise ValueError("'{0}' is not a supported audio file: no audio streams found".format(filepath))

    info_dictionary = {
        'file_type': audio_stream['codec_name'],
        'sample_rate': audio_stream['sample_rate'],
        'channels': audio_stream['channels'],
        'duration': probe_dict['format']['duration'],
        'bit_rate': probe_dict['format']['bit_rate'],
        'encoding': audio_stream['codec_long_name'],
    }

    if 'tags' in probe_dict['format']:
        info_dictionary['tags'] = probe_dict['format']['tags']

    return info_dictionary

if __name__ == '__main__':
    from argparse import ArgumentParser
    from pprint import pprint

    # service.py executed as script
    parser = ArgumentParser(description='Call ffprobe and get meta info back.')
    parser.add_argument('file')

    args = parser.parse_args()

    pprint(scan(args.file))
