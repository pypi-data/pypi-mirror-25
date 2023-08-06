#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile

import pytest

from supportdata.supportdata import download_file


def test_download_file_nooutput():
    """ download_file requires a valid outputdir
    """
    try:
        download_file('non/existent/path', url=None, filename=None)
    except:
        return
    assert False, "download_file should fail if output path is invalid"


def test_download_file():
    download_file(
            tempfile.gettempdir(),
            "https://raw.githubusercontent.com/castelao/supportdata/master/LICENSE",
            "LICENSE")
    filename = os.path.join(tempfile.gettempdir(), "LICENSE")
    assert os.path.exists(filename)
    os.remove(filename)


def test_download_CARS():
    """ Test with a large gz file

        This is a real test with a few hundreds MB gzipped file. CARS is a
          climatology used by oceansdb package.

        Maybe change this test in the future to use another file, but still
          I should use a large gzipped file.
    """
    url = "http://www.marine.csiro.au/atlas/export/temperature_cars2009a.nc.gz"
    filename = 'temperature_cars2009a.nc'
    download_file(
            outputdir=tempfile.gettempdir(),
            url=url,
            filename=filename,
            md5hash='a310418e6c36751f2f9e9e641905d503')
    filename = os.path.join(tempfile.gettempdir(), filename)
    assert os.path.exists(filename)
    os.remove(filename)


def test_download_file_md5():
    url = "https://raw.githubusercontent.com/castelao/supportdata/master/LICENSE"
    md5hash = "bcc8d2a90ed7d99dc34a3d6938bd672d"

    download_file(tempfile.gettempdir(), url, 'LICENSE', md5hash)
    output = os.path.join(tempfile.gettempdir(), 'LICENSE')
    assert os.path.exists(output)
    os.remove(output)

    try:
        download_file(tempfile.gettempdir(), url, 'LICENSE', 'bad hash')
    except:
        return

    assert False, "download_file didn't fail with a bad hash"
