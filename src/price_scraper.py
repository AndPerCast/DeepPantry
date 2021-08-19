"""Real-time web scraper for product prices.

This module aims at easing product price
information gathering from a certain website.

Author:
    Andrés Pérez
"""

from bs4 import BeautifulSoup
import requests
from typing import Tuple, List


SOURCE_URL: str = "https://www.trolley.co.uk"
"""Base website url to scrape data from."""


def scrape_price(product_name: str,
                 parser: str = "html.parser") -> Tuple[str, float, str]:
    """Retrieves price information for given product.

    Args:
        product_name: Common name for a product.
        parser: HTML parser used by the scraper.

    Returns:
        Purchase link, price and currency.

        Default values will be returned if such gathering
        process fails, as shown in the example.

    Example::

        >>> scrape_price("soda")
        ('https://www.trolley.co.uk/product/vive-soda-water/FTB465', 0.25, '£')
        
        >>> scrape_price("?")
        ("", 0.0, "")
    """
    # Make a complete url to fetch data for given product.
    url: str = f"{SOURCE_URL}/search/?q={product_name.lower()}"
    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, parser)
    except (requests.ConnectionError, requests.Timeout, requests.HTTPError):
        return "", 0.0, ""
    
    product_data: List[Tuple[str, float, str]] = []
    # Find all product entries and extract data from their descendent tags.
    for product in soup.find_all("div", class_="product-listing"):
        link: str = SOURCE_URL + product.a["href"]
        # Ignore extra price data from descendent tags.
        price_str = str(product.a.find("div", class_="_price").contents[0])
        price = float(price_str[1:])
        currency = price_str[0]
        product_data.append((link, price, currency))
    # Find product with lowest price.
    return min(product_data, key=lambda data: data[1], default=("", 0.0, ""))
