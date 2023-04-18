from imgurpython import ImgurClient
import requests
from bs4 import BeautifulSoup

client_id = "d04108c95afbb8d"


class EbayTool:
    def __init__(self, imgur_secret: str = None) -> None:
        self.imgur_secret = imgur_secret

    def imgur_upload(self, href: str) -> str:
        """Duplicates an image to imgur.

           This allows for non permanant image links to be duplicated from ebay
           to a more permanant source.

        Args:
            href: A link to an image resource.

        Returns:
            A new href string to an imgur image that has duplicated the source passed to it.

        """
        try:
            client = ImgurClient(client_id, self.imgur_secret)
            return client.upload_from_url(href)["link"]
        except Exception as e:
            print(
                "Upload to imgur failed, this is likely due to class being intialized without imgur_secret",
                e,
            )

        return None

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
        for link in soup.find(
            "div", class_="ux-image-carousel-item active image"
        ).find_all("img"):
            src = link.get("src")
            if src:
                return src

        return None
