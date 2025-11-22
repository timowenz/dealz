from playwright.async_api import Page


class AmazonCrawler:
    def __init__(self) -> None:
        self.timeout = 10000

    async def get_latest_price_info(self, page: Page) -> dict | None:
        price_whole_element = await page.wait_for_selector(
            '[data-csa-c-pos="1"] .a-price-whole', timeout=self.timeout
        )
        price_whole_text = await price_whole_element.text_content()
        price_fraction_element = await page.wait_for_selector(
            '[data-csa-c-pos="1"] .a-price-fraction', timeout=self.timeout
        )
        price_fraction_text = await price_fraction_element.text_content()
        price_whole_clean = price_whole_text.strip().replace(",", "").replace(".", "")
        price_fraction_clean = (
            price_fraction_text.strip() if price_fraction_text else "00"
        )

        return (price_whole_clean, price_fraction_clean)
