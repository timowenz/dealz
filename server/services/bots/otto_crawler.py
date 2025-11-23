from playwright.async_api import Page


class OttoCrawler:
    def __init__(self) -> None:
        self.timeout = 10000

    async def get_latest_price_info(self, page: Page, product_name: str) -> dict | None:
        product_tiles = await page.query_selector_all("li.find_tile")

        for tile in product_tiles:
            title_element = await tile.query_selector(".find_tile__name")
            if not title_element:
                continue

            title_text = await title_element.text_content()
            if not title_text:
                continue

            def normalize(s: str) -> str:
                return "".join(c.lower() for c in s if c.isalnum())

            norm_product = normalize(product_name)
            norm_title = normalize(title_text)

            if norm_product in norm_title:
                price_element = await tile.query_selector(".find_tile__retailPrice")
                if not price_element:
                    continue

                price_text = await price_element.text_content()
                if not price_text:
                    continue

                price_text_clean = (
                    price_text.strip()
                    .replace("\xa0", " ")
                    .replace("€", "")
                    .replace("ab", "")
                    .strip()
                )
                if "," in price_text_clean:
                    euro, cent = price_text_clean.split(",", 1)
                elif "." in price_text_clean:
                    euro, cent = price_text_clean.split(".", 1)
                else:
                    euro, cent = price_text_clean, "00"

                euro = "".join(filter(str.isdigit, euro))
                cent = "".join(filter(str.isdigit, cent.strip()))[:2] if cent else "00"

                return (euro, cent)

        return None
