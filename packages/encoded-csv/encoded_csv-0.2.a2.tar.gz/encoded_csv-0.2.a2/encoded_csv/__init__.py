#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Intelligently read encoded CSV files.

This module provides a single function: get_csv(), which is used to read
an encoded CSV file.
"""


import chardet
import codecs
import csv
import io
from itertools import islice
import os


def get_csv(
    csv_file,
    skip_lines=0,
    encoding='',
    dialect='',
    fieldnames=[],
    sample_lines=100
):
    """Read content from an encoded CSV file.

    We assume first row (after discarding any header lines) has column names.

    Keyword arguments:
    csv_file -- path to CSV file to open
    skip_header_lines -- (optional) number of lines to discard in the
        assumption that they constitute a file header of some sort (default is
        to skip no lines)
    encoding -- (optional) specifies the encoding which is to be used for the
        file; the standard python codecs module is used, so any of the
        standard encodings may be specified; default behavior is to attempt
        best guess using chardet)
    dialect -- (optional) a set of parameters specific to a particular CSV
        dialect; the standard python csv module is used, so the standard,
        predefined dialect values or formatting parameters must be used;
        default behavior is to attempt best guess using csv.Sniffer.
    fieldnames -- (optional) is used to force the csv.DictReader to use a
        particular set of fieldnames.
    sample_lines -- (optional) integer used to prepare the sample given to
    csv.Sniffer() when attempting to detect the CSV dialect in use; default is
    100 lines or the entire file, whichever is fewer.
    """
    rpath = os.path.realpath(csv_file)

    reader_kwargs = {}

    # encoding detection
    if encoding == '':
        num_bytes = min(1024, os.path.getsize(rpath))
        raw = open(rpath, 'rb').read(num_bytes)
        if raw.startswith(codecs.BOM_UTF8):
            file_encoding = 'utf-8-sig'
        else:
            file_encoding = chardet.detect(raw)['encoding']
    else:
        file_encoding = encoding

    # force fieldnames if necessary
    if len(fieldnames) != 0:
        reader_kwargs['fieldnames'] = fieldnames

    with io.open(rpath, 'r', encoding=file_encoding) as f:

        # dialect detection
        if dialect == '':
            for _ in range(skip_lines):
                next(f)
            sample = []
            for _ in range(sample_lines):
                sample.append(f.readline())
            sample = ''.join(sample)
            sniffer = csv.Sniffer()
            reader_kwargs['dialect'] = sniffer.sniff(sample)
        else:
            reader_kwargs['dialect'] = dialect

        # read into a list of dictionaries
        f.seek(0)
        content = []
        reader = csv.DictReader(islice(f, skip_lines, None), **reader_kwargs)
        for row in reader:
            content.append(row)

    if len(content) > 0:
        return (
            {
                'content': content,
                'fieldnames': list(content[0].keys()),
                'encoding': file_encoding,
                'dialect': reader_kwargs['dialect']
            })
    else:
        return None
