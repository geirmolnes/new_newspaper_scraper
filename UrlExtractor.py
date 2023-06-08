from typing import Optional
from urllib.parse import urlparse
import requests


class UrlExtractor:
    def __init__(self, newspaper_name, url):
        self.newspaper_name = newspaper_name
        self.url = url

        self.canonical_url_extractors = {
            "vg": self.get_vg_canonical_url,
            "dn": self.get_dn_canonical_url,
            "aftenposten": self.get_aftenposten_url,
            "e24": self.get_e24_canonical_url,
            "nrk": self.get_nrk_url,
            "nettavisen": self.get_nettavisen_url,
            "finansavisen": self.get_finansavisen_url,
            "tv2": self.get_tv2_url,
            "vl": self.get_vl_url,
            "dagsavisen": self.get_dagsavisen_url,
            "filternyheter": self.get_filter_url,
        }

    def extract_canonical_url(self):
        """
        Attempts to extract the canonical URL for a given newspaper.

        If the newspaper's name is in the extractor dictionary, applies the corresponding extractor function.
        If not, returns the original URL.

        In case of an exception, prints an error and returns the original URL.
        """
        try:
            if self.newspaper_name in self.canonical_url_extractors:
                return self.canonical_url_extractors[self.newspaper_name]()
            else:
                return self.url
        except Exception as e:
            print(
                f"Error extracting canonical url: {self.url}\n{e}\nreturning non canonical url\n"
            )
            return self.url

    def get_vg_canonical_url(self):
        return self._get_schibsted_url()

    def get_aftenposten_url(self):
        return self._get_schibsted_url()

    def get_tv2_url(self):
        return self.url

    def get_vl_url(self):
        return self.url

    def get_dagsavisen_url(self):
        return self.url

    def get_filter_url(self):
        return self.url

    def get_e24_canonical_url(self):
        return self._get_schibsted_url()

    def _get_schibsted_url(self):
        base_url = f"https://www.{self.newspaper_name}.no/i/"  # remember the 'i' here
        url_key = self.url.split("/i/")[1].split("/")[0]
        return base_url + url_key

    def get_nrk_url(self):  # sourcery skip: class-extract-method
        base_url = f"https://www.{self.newspaper_name}.no/"
        url_key = self.url.split("-")[-1]
        return base_url + url_key

    def get_dn_canonical_url(self):
        parsed_url = urlparse(self.url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}/{parsed_url.path.split('/')[-1]}"

    def get_nettavisen_url(self):
        base_url = f"https://www.{self.newspaper_name}.no/"
        url_key = self.url.split("/")[-1]
        return base_url + url_key

    def get_finansavisen_url(self):
        base_url = f"https://www.{self.newspaper_name}.no/"
        url_key = self.url.split("/")[-2]
        return base_url + url_key


def clean_source_url(url):
    pattern = "?utm_source="
    return url.split(pattern)[0] if pattern in url else url


def get_canonical_url(newspaper_name: str, url: str) -> Optional[str]:
    url = clean_source_url(url)
    extractor = UrlExtractor(newspaper_name, url)
    canonical_url = extractor.extract_canonical_url()
    return canonical_url if verify_url(canonical_url) else url


def verify_url(url: str) -> bool:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error verifying url: {url}:\n{e}\nreturning non canonical url\n")
        return False
