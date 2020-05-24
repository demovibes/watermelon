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
    if probe_dict['format']['nb_streams'] != 1 or probe_dict['streams'][0]['codec_type'] != 'audio':
        raise ValueError("'{0}' is not a supported audio file".format(filepath))

    return {
        'file_type': probe_dict['streams'][0]['codec_name'],
        'sample_rate': probe_dict['streams'][0]['sample_rate'],
        'channels': probe_dict['streams'][0]['channels'],
        'duration': probe_dict['format']['duration'],
        'bit_rate': probe_dict['format']['bit_rate'],
        'encoding': probe_dict['streams'][0]['codec_long_name'],
    }

if __name__ == '__main__':
    import argparse
    from pprint import pprint

    # service.py executed as script
    parser = argparse.ArgumentParser(description='Call ffprobe and get meta info back.')
    parser.add_argument('file')

    args = parser.parse_args()

    pprint(scan(args.file))
