from playwright.async_api import async_playwright, Page
from simulator.page.login_page import LoginPage
from simulator.page.main_page import MainPage
from typing import Union, TYPE_CHECKING
from functools import wraps

if TYPE_CHECKING:
    from simulator import Simulator

def update_current_page(func):
    @wraps(func)
    async def wrapper(self: 'Simulator', *args, **kwargs):
        result = await func(self, *args, **kwargs)
        self.current_page = result if result else self.current_page
        return result
    return wrapper


class Simulator:
    def __init__(self):
        self.current_page = None
        self.pages = {
            'LoginPage': LoginPage(),
            'MainPage': MainPage()
        }

    @property
    def page(self) -> Union[LoginPage, MainPage]:
        return self.pages[self.current_page]

    @update_current_page
    async def login(self, page: Page, id: str, password: str):
        await page.goto('https://www.threekingdom100.com/')
        self.current_page = 'LoginPage'
        return await self.page.login(page, id, password)

        ## Login인지 Main인지 판단, 하지만 일단 Login으로 전제하고 구현


simulator = Simulator()

async def crawl_website(content: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page: Page = await browser.new_page()

        id: str = '01011111111'
        password: str = '1111'
        await simulator.login(page, id, password)

        # await simulator.language('Korean')
        # await simulator.season(2)

        crawled_content = await page.content()
        await browser.close()

    return crawled_content[:100] + ' From UDP Server by python'