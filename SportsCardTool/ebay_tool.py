import requests
from bs4 import BeautifulSoup

client_id = "d04108c95afbb8d"


class EbayTool:
    def __init__(self, imgur_secret: str = None) -> None:
        self.imgur_secret = imgur_secret

    def parse_ebay_listing(self, href: str) -> str:
        """Gathers primary image from ebay listing

           Gathers image in primary panel in a given ebay link to a listing.
           May fail if passed some modified ebay link or search result.

        Args:
            href: A link to an ebay listing.

        Returns:
            The source href string of the primary image in listing.

        """
        soup = BeautifulSoup(requests.get(href).content, "lxml")
        for link in soup.find("div", class_="ux-image-carousel-item active image").find_all("img"):
            src = link.get("src")
            return src
