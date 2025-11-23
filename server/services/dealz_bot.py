from datetime import datetime
from enum import Enum
from urllib.robotparser import RobotFileParser
import httpx
from playwright.async_api import async_playwright
from sqlmodel import Session

from models.dealz import PriceHistory
from models.dealz import Dealz
from services.bots.amazon_crawler import AmazonCrawler
from services.bots.otto_crawler import OttoCrawler


class SupportedBaseWebsiteURLs(Enum):
    AMAZON = "https://www.amazon.de"  # Search query is: https://www.amazon.de/s?k=...
    OTTO = "https://www.otto.de"  # Search query is: https://www.otto.de/suche/...


class DealzBot:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.headless = True
        self.USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:145.0) Gecko/20100101 Firefox/145.0"

    async def search_prices(self, product_name: str) -> dict:
        # Steps:
        # 1. Check if bot is allowed
        # 2. HTTP requests
        # 3. Browser automation when necessary
        # Finished
        results = {}
        for site in SupportedBaseWebsiteURLs:
            if not self.is_robots_txt_valid(url=site.value):
                results[site.name] = {
                    "url": site.value,
                    "price": None,
                    "product_name": product_name,
                    "error": "Not allowed by robots.txt",
                }
                continue

            price: int | None = await self.crawl_latest_price(
                url=site.value, product_name=product_name
            )

            # Results returning for API
            results[site.name] = {
                "url": self._get_product_url(
                    base_url=site.value, product_name=product_name
                ),
                "price": price,
            }
        return results

    def is_robots_txt_valid(self, url: str) -> bool:
        robot = RobotFileParser(f"{url}/robots.txt")
        robot.read()

        return robot.can_fetch(useragent=self.USER_AGENT, url=url)

    def _get_product_url(self, base_url: str, product_name: str) -> str:
        sanitized_product_name = product_name.replace(" ", "+")
        if "amazon" in base_url:
            return f"{base_url}/s?k={sanitized_product_name}"
        elif "otto" in base_url:
            return f"{base_url}/suche/{sanitized_product_name}"
        else:
            raise ValueError(f"Unknown or unsupported base url: {base_url}")

    async def crawl_latest_price(self, url: str, product_name: str) -> int | None:
        product_url = self._get_product_url(url, product_name)
        print(product_url)
        response = httpx.get(product_url)
        # print(response.text)
        if response.status_code != 200:
            # await self.crawl_with_browser(url=product_url)
            # return None
            print(
                "HTTP response was not successful. Status Code:", response.status_code
            )

        price_in_cents = await self.crawl_with_browser(
            url=product_url, product_name=product_name
        )

        self._insert_price_into_database(
            price_in_cents=price_in_cents, url=url, product_name=product_name
        )

        return price_in_cents

    async def crawl_with_browser(self, url: str, product_name: str) -> int | None:
        async with async_playwright() as playwright:
            chromium = playwright.chromium
            browser = await chromium.launch(headless=self.headless)
            page = await browser.new_page()
            await page.goto(url)

            try:
                print("URL:", url)

                price_info = None

                match True:
                    case _ if "amazon" in url:
                        amazon_crawler = AmazonCrawler()
                        price_info = await amazon_crawler.get_latest_price_info(
                            page=page, product_name=product_name
                        )
                    case _ if "otto" in url:
                        otto_crawler = OttoCrawler()
                        price_info = await otto_crawler.get_latest_price_info(
                            page=page, product_name=product_name
                        )

                if price_info:
                    euro_price, cent_price = price_info
                    price_in_cents = int(euro_price + cent_price)
                    # print(f"Price found: {euro_price}.{cent_price} EUR")
                    return price_in_cents

                print(f"Price not found for {url}")
                return None
            except Exception as e:
                print(f"Could not find price element: {e}")
            # await page.wait_for_timeout(100000)
            await browser.close()
        return None

    def _insert_price_into_database(
        self, price_in_cents: int | None, url: str, product_name: str
    ):
        try:
            dealz = (
                self.db.query(Dealz).filter(Dealz.product_name == product_name).first()
            )

            if not dealz:
                dealz = Dealz(
                    product_name=product_name,
                    currency="EUR",
                    lowest_price=price_in_cents,
                )
                self.db.add(dealz)
                self.db.flush()

            price_history = PriceHistory(
                deal_id=dealz.id,
                price_in_cents=price_in_cents,
                url=url,
                merchant=self._extract_merchant_from_url(url=url),
            )
            self.db.add(price_history)

            if price_in_cents is not None and (
                dealz.lowest_price is None or price_in_cents < dealz.lowest_price
            ):
                dealz.lowest_price = price_in_cents
                dealz.updated_at = datetime.now()

            if self.db is None:
                self.db.commit()
        except Exception:
            if self.db is None:
                self.db.rollback()
            raise
        finally:
            if self.db is None:
                self.db.close()

    def _extract_merchant_from_url(self, url: str) -> str:
        if "amazon" in url:
            return "Amazon"
        if "otto" in url:
            return "Otto"
        return "Unknown"
