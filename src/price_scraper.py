"""
"""

from bs4 import BeautifulSoup
import requests
from typing import Tuple, List

SOURCE_URL: str = "https://www.trolley.co.uk"

def scrape_price(product_name: str,
                 parser: str = "html.parser") -> Tuple[str, float, str]:
    """
    """
    url: str = f"{SOURCE_URL}/search/?q={product_name.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, parser)
    except (requests.ConnectionError, requests.Timeout, requests.HTTPError):
        return ("", 0.0, "")
    
    product_data: List[Tuple[str, float, str]] = []
    for product in soup.find_all("div", class_="product-listing"):
        link: str = SOURCE_URL + product.a["href"]
        price_str = str(product.a.find("div", class_="_price").contents[0])
        price = float(price_str[1:])
        currency = price_str[0]
        product_data.append((link, price, currency))
    return min(product_data, key=lambda data: data[1], default=("", 0.0, ""))
