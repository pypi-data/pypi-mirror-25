import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from .errors import (
    WikiConnectionError, DumpCompletionStateUncertainError,
    NoCompleteDumpsError
)
from .config import ENDPOINT_URL


class DumpMetadata(object):

    def __init__(self, wiki, date=None):
        self._html_cache = {}
        self._wiki = wiki
        if date is None:
            date = self._most_recent_completed_dump_date()
        self._date = date
        self._init_sha_map()
        self._init_file_url_map()

    @property
    def date(self):
        return self._date

    def file_urls(self, matching):
        matching_file_urls = {}
        for filename, url in self._file_url_map.items():
            matching_regex = [
                r for r in matching
                if re.search(r, filename)
            ]
            if len(matching_regex) > 0:
                matching_file_urls[filename] = url
        return matching_file_urls

    def dump_dates(self):
        result = []
        html = self._get_html('/'.join([ENDPOINT_URL, self._wiki]))
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            match = re.match(r'(\d{8})', link.text)
            if match is not None:
                result.append(datetime.strptime(match.group(1), '%Y%m%d'))
        return result

    def sha_for(self, filename):
        return self._sha_map[filename]

    def _get_html(self, url):
        if url in self._html_cache:
            result = self._html_cache[url]
        else:
            r = requests.get(url)
            if r.status_code != 200:
                raise WikiConnectionError(url)
            result = r.text
            self._html_cache[url] = result
        return result

    def _validate_date(self):
        available_dump_dates = self.dump_dates()
        if self._date not in available_dump_dates:
            raise NoCompleteDumpsError()

    def _get_dump_page_html(self, dump_date):
        date_str = dump_date.strftime('%Y%m%d')
        return self._get_html(
            "/".join([ENDPOINT_URL, self._wiki, date_str])
        )

    def _is_dump_complete(self, dump_date):
        html = self._get_dump_page_html(dump_date)
        soup = BeautifulSoup(html, 'html.parser')
        if len(soup.findAll("span", {"class": "in-progress"})) == 1:
            return False
        if len(soup.findAll("span", {"class": "done"})) == 1:
            return True
        raise DumpCompletionStateUncertainError()

    def _most_recent_completed_dump_date(self):
        available_dump_dates = self.dump_dates()
        while len(available_dump_dates) > 0:
            recent = max(available_dump_dates)
            if self._is_dump_complete(recent):
                return recent
            else:
                available_dump_dates.remove(recent)
        raise NoCompleteDumpsError()

    def _init_sha_map(self):
        sha_map = {}
        date_str = self._date.strftime('%Y%m%d')
        sha1_file = '{0}-{1}-sha1sums.txt'.format(self._wiki, date_str)
        url = self._get_file_url(sha1_file)
        content = self._get_html(url)
        for line in content.strip().split('\n'):
            sha1, filename = line.split()
            sha_map[filename] = sha1
        self._sha_map = sha_map

    def _init_file_url_map(self):
        self._file_url_map =  dict([(filename, self._get_file_url(filename))
                     for filename in self._sha_map])

    def _get_file_url(self, filename):
        date_str = self._date.strftime('%Y%m%d')
        return '/'.join([ENDPOINT_URL, self._wiki, date_str, filename])
