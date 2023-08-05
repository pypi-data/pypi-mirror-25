import os.path
from .dumpmetadata import DumpMetadata
from .config import DEFAULT_WIKI, DEFAULT_THREAD_COUNT
from .downloader import download_files_in_map



class Dump(object):

    def __init__(self, wiki=DEFAULT_WIKI, date=None):
        self._metadata = DumpMetadata(wiki, date)
        self.wiki = wiki
        self.date = self._metadata.date

    def download(
        self, output_dir, matching=['.*'], threads=DEFAULT_THREAD_COUNT
    ):
        full_path_url_sha_list = []
        file_urls = self._metadata.file_urls(matching)
        for filename, url in file_urls.items():
            full_path_url_sha_list.append(
                (
                    os.path.join(output_dir, filename),
                    url,
                    self._metadata.sha_for(filename)
                )
            )
        download_files_in_map(full_path_url_sha_list, threads)
