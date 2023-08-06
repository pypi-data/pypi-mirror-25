# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from sys import stdout
import shutil
import hashlib
from tempfile import NamedTemporaryFile
from gzip import GzipFile
from zipfile import ZipFile

from six.moves.urllib.request import urlopen
from six.moves.urllib.parse import urlsplit
from filelock import FileLock


def download_file(outputdir, url, filename=None, md5hash=None, progress=True):
    """ Download data file from a URL

        outputdir: Where to save the downloaded file.
        url: Source URL, what to download.
        filename: Save downloaded file as this name. If not given, uses the
          original name from the url.
        md5hash: If given, check if the downloaded file match with the expected
          hash.
    """
    block_size = 131072

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    #assert os.path.exists(outputdir)

    isgzfile = False
    iszipfile = False

    remote_filename = os.path.basename(urlsplit(url)[2])
    if remote_filename[-3:] == '.gz':
        isgzfile = True
    elif remote_filename[-4:] == '.zip':
        iszipfile = True

    if filename is None:
        if isgzfile:
            filename = remote_filename[:-3]
        else:
            filename = remote_filename
    elif filename[-3:] == '.gz':
        # Take it back. Looks like the user wants to save a gzipped file
        isgzfile = False

    fname = os.path.join(outputdir, filename)
    if os.path.isfile(fname):
        return fname

    flock = os.path.join(outputdir, ".%s.lock" % filename)
    lock = FileLock(flock)
    with lock.acquire(timeout=900):
        md5 = hashlib.md5()

        remote = urlopen(url)

        try:
            file_size = int(remote.headers["Content-Length"])
            print("Downloading: %s (%d bytes)" % (filename, file_size))
        except:
            file_size = 1e30
            print("Downloading unknown size file")

        with NamedTemporaryFile(delete=True) as f:
            bytes_read = 0
            for block in iter(lambda: remote.read(block_size), b''):
                f.write(block)
                md5.update(block)
                bytes_read += len(block)

                if progress:
                    status = "\r%10d [%6.2f%%]" % (
                            bytes_read, bytes_read*100.0/file_size)
                    stdout.write(status)
                    stdout.flush()
            if progress:
                print('')

            if md5hash is not None:
                assert md5hash == md5.hexdigest(), \
                        "Downloaded file (%s) doesn't match expected content" \
                        "(md5 hash: %s)" % (filename, md5.hexdigest())

            if isgzfile or iszipfile:
                f.seek(0)
                print('Decompressing downloaded file')
                if isgzfile:
                    fz = GzipFile(f.name, 'rb')
                elif iszipfile:
                    fz = ZipFile(f.name, 'rb')
                with open(fname, 'wb') as fout:
                    for block in iter(lambda: fz.read(block_size), b''):
                        fout.write(block)
            else:
                shutil.copy(f.name, fname)

    print("Downloaded: %s" % fname)
    return fname
