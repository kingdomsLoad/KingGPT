from playwright.async_api import Page
from interface.Page import IPage

class MainPage(IPage):
    async def navigate(self, page: Page, next_page: str):
        return await super().navigate(page, next_page)