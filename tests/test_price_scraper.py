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

from price_scraper import scrape_prices


class TestPriceScraper(unittest.TestCase):
    """Tests price_scraper module functionality"""

    @classmethod
    def setUpClass(cls) -> None:
        with open(HTML_TEST_FILE, "r", newline="", encoding="utf-8") as f:
            cls.html_text = f.read()
        cls.product_names = [basename(HTML_TEST_FILE).split("-")[0]]
        cls.price_info = [(
            cls.product_names[0],
            'https://www.trolley.co.uk/product/morrisons-savers-honey/IBN007',
            0.69,
            '£',
        )]
        cls.default_price_info = [(cls.product_names[0], "", 0.0, "")]

    def setUp(self) -> None:
        if not self.html_text:
            self.skipTest("Cannot read any content from html test file")

    def test_scrape_prices(self) -> None:
        with patch("price_scraper.requests.Session.get") as mocked_get:
            # Check if correct price information is retrieved.
            requests.Response.text = self.html_text
            r = requests.Response()
            r.status_code = 200
            mocked_get.return_value = r
            self.assertListEqual(self.price_info,
                                 scrape_prices(self.product_names))
            
            # Check if connection related errors induce default values.
            r = requests.Response()
            r.status_code = 500
            mocked_get.return_value = r
            self.assertListEqual(self.default_price_info,
                                 scrape_prices(self.product_names))

            mocked_get.side_effect = requests.ConnectionError
            self.assertListEqual(self.default_price_info,
                                 scrape_prices(self.product_names))

            mocked_get.side_effect = requests.Timeout
            self.assertListEqual(self.default_price_info,
                                 scrape_prices(self.product_names))
            
            # Check if a lack of products induces default values.
            mocked_get.reset_mock(side_effect=True)
            requests.Response.text = "<html></html>"
            r = requests.Response()
            r.status_code = 200
            mocked_get.return_value = r
            self.assertListEqual(self.default_price_info,
                                 scrape_prices(self.product_names))
            

if __name__ == "__main__":
    unittest.main()
