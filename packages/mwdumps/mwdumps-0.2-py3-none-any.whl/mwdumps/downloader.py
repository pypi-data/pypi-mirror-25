import os.path
import urllib
import hashlib
import logging
from multiprocessing.pool import ThreadPool
from .config import MAX_RETRIES
from random import randint


def download_files_in_map(file_url_shas, threads=1):
    with ThreadPool(threads) as pool:
        pool.map(_thread_download_star, file_url_shas)


def _thread_download_star(args):
    _thread_download(*args)


def _thread_download(path, url, sha):
    if os.path.isfile(path):
        if _check_sha_is_correct(path, sha):
            logging.info('Using existing file at {0}'.format(path))
            return
        else:
            logging.info('{0} corrupt. Downloading new.'.format(path))

    for i in range(MAX_RETRIES):
        logging.info('{0} <-- {1}'.format(path, url))
        opener = urllib.request.URLopener()
        opener.retrieve(url, path)
        if _check_sha_is_correct(path, sha):
            logging.info('{0} complete.'.format(path))
            break
        else:
            logging.warning('{0} download failed. Retrying.'.format(url))
    else:
        logging.error('{0} failed to download'.format(url))


def _check_sha_is_correct(filepath, sha):
    sha_gen = hashlib.sha1()
    chunksize = 1024*1024*5
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(chunksize)
            if not chunk:
                break
            sha_gen.update(chunk)
    return sha == sha_gen.hexdigest()
