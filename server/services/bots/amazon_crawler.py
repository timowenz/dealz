from playwright.async_api import Page


class AmazonCrawler:
    def __init__(self) -> None:
        self.timeout = 10000

    async def get_latest_price_info(self, page: Page, product_name: str) -> dict | None:
        search_results = await page.query_selector_all(
            'div[data-component-type="s-search-result"]'
        )

        for result in search_results:
            title_element = await result.query_selector("h2")
            if not title_element:
                continue

            title_text = await title_element.text_content()
            if not title_text:
                continue

            if product_name.lower() in title_text.lower():
                price_whole_element = await result.query_selector(".a-price-whole")
                price_fraction_element = await result.query_selector(
                    ".a-price-fraction"
                )

                if price_whole_element and price_fraction_element:
                    price_whole_text = await price_whole_element.text_content()
                    price_fraction_text = await price_fraction_element.text_content()

                    price_whole_clean = (
                        price_whole_text.strip().replace(",", "").replace(".", "")
                    )
                    price_fraction_clean = (
                        price_fraction_text.strip() if price_fraction_text else "00"
                    )

                    return (price_whole_clean, price_fraction_clean)

        return None
