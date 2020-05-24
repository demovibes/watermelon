#!/usr/bin/env python

"""
soxi scan connector for watermelon

Given a filename on command line, calls soxi, and returns key-value data for
insert into the DB.
"""

from os.path import getsize

from sox import file_info


def scan(filepath):
    # sox package has an info() but it should not be used:
    #  it's just a wrapper that calls a set of functions
    #  and returns them in a dict
    # ...and the functions are the wrong ones :)

    info_dictionary = {
        'file_type': file_info.file_type(filepath),
        'sample_rate': round(file_info.sample_rate(filepath)),
        'channels': file_info.channels(filepath),
        'duration': file_info.duration(filepath),
#        'bit_rate': file_info.bitrate(filepath),
        'encoding': file_info.encoding(filepath),
    }

    # bitrate is currently broken (1.37) but we can fake it
    info_dictionary['bit_rate'] = round(getsize(filepath) / info_dictionary['duration'] * 8)
    return info_dictionary

if __name__ == '__main__':
    import argparse
    from pprint import pprint

    # service.py executed as script
    parser = argparse.ArgumentParser(description='Call soxi and get meta info back.')
    parser.add_argument('file')

    args = parser.parse_args()

    pprint(scan(args.file))
