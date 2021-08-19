"""Unit Testing for price_scraper module.

Author:
    Andrés Pérez
"""

import unittest
from unittest.mock import patch
import requests
import sys
from os.path import join, dirname, basename

# Add tested modules to Python path.
sys.path.insert(0, join(dirname(dirname(__file__)), "src"))

# Make sure to use this naming format: <product_name>-<website_name>-test.txt
HTML_TEST_FILE: str = join(dirname(__file__), "honey-Trolley.co.uk-test.txt")

from price_scraper import scrape_price


class TestPriceScraper(unittest.TestCase):
    """Tests price_scraper module functionality"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.html_text: str = ""
        with open(HTML_TEST_FILE, "r", newline="", encoding="utf-8") as f:
            cls.html_text = f.read()
        cls.product_name: str = basename(HTML_TEST_FILE).split("-")[0]
        cls.price_info = ('https://www.trolley.co.uk/product/morrisons-savers-honey/IBN007', 0.69, '£')
        cls.default_price_info = ("", 0.0, "")

    def setUp(self) -> None:
        if not self.html_text:
            self.skipTest("Cannot read any content from html test file")

    def test_scrape_price(self) -> None:
        self.assertTupleEqual(self.price_info, scrape_price(self.product_name))

        with patch("price_scraper.requests.get") as mocked_get:
            r = requests.Response()
            r.status_code = 500
            mocked_get.return_value = r

            self.assertTupleEqual(self.default_price_info,
                                  scrape_price(self.product_name))


if __name__ == "__main__":
    unittest.main()
