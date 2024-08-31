from playwright.async_api import async_playwright, Page, Browser, Playwright
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

class PlaywrightContent:
    def __init__(self):
        self.browser: Browser = None
        self.page: Page = None

class Simulator:
    def __init__(self):
        self.pw = PlaywrightContent()
        self.current_page = None
        self.pages = {
            'LoginPage': LoginPage(),
            'MainPage': MainPage()
        }

    async def start_browser(self, playwright: Playwright):
        self.pw.browser = await playwright.chromium.launch(headless=False)
        context = await self.pw.browser.new_context(ignore_https_errors=True)  # 새로운 컨텍스트 생성 (기본적으로 시크릿 모드와 유사)
        self.pw.page = await context.new_page()

    async def close_browser(self):
        await self.pw.browser.close()

    @property
    def page(self) -> Union[LoginPage, MainPage]:
        return self.pages[self.current_page]

    @update_current_page
    async def login(self, id: str, password: str):
        await self.pw.page.goto('https://www.threekingdom100.com/')
        self.current_page = 'LoginPage'
        return await self.page.login(self.pw.page, id, password)
        ## Login인지 Main인지 판단, 하지만 일단 Login으로 전제하고 구현
    
    async def language(self, language: str):
        await self.page.change_language(self.pw.page, language)

    async def season(self, season: str):
        await self.page.change_season(self.pw.page, season)

simulator = Simulator()

async def crawl_website(content: str) -> str:
    async with async_playwright() as p:
        await simulator.start_browser(p)

        id: str = '01011111111'
        password: str = '1111'
        await simulator.login(id, password)
        await simulator.language("한국어")
        await simulator.season('2')

        crawled_content = await simulator.pw.page.content()
        await simulator.close_browser()

    return crawled_content[:100] + ' From UDP Server by python'