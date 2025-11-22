from playwright.async_api import Page


class OttoCrawler:
    def __init__(self) -> None:
        self.timeout = 10000

    async def get_latest_price_info(self, page: Page) -> dict | None:
        article = page.locator("#reptile-tilelist > article").nth(2)
        price_element = article.locator(
            "ul > li > div > div:nth-child(2) > div:nth-child(5) > div > span.find_tile__retailPrice"
        )
        await price_element.wait_for(timeout=self.timeout)
        price_text = await price_element.text_content()
        if not price_text:
            return None

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

        # await page.wait_for_timeout(20000)

        return (euro, cent)
