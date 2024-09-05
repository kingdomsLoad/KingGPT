from playwright.async_api import async_playwright, Page, Browser, Playwright
from simulator.page.login_page import LoginPage
from simulator.page.main_page import MainPage
from simulator.page.deck_edit_page import DeckEditPage
from typing import Union, TYPE_CHECKING, List
from functools import wraps
from simulator.path_finder.path_finder import bfs_all_paths, get_path


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
        self.context: Browser.new_context = None
        self.page: Page = None

class Simulator:
    def __init__(self):
        self.pw = PlaywrightContent()
        self.current_page = None
        self.pages = {
            'LoginPage': LoginPage(),
            'MainPage': MainPage(),
            'DeckEditPage': DeckEditPage()
        }
    async def start_browser(self, playwright: Playwright):
        self.pw.browser = await playwright.chromium.launch(headless=False)
        self.pw.context = await self.pw.browser.new_context(ignore_https_errors=True)  # 새로운 컨텍스트 생성 (기본적으로 시크릿 모드와 유사)
        self.pw.page = await self.pw.context.new_page()

    async def close_browser(self):
        await self.pw.browser.close()

    @property
    def page(self) -> Union[LoginPage, MainPage, DeckEditPage]:
        return self.pages[self.current_page]

    async def navigate(self, target_page: str):
        if self.current_page == target_page:
            return
        
        path = get_path(self.current_page, target_page)
        for i in range(len(path) - 1):
            next_page = path[i + 1]
            await self.page.navigate(self.pw.page, next_page)
        
        self.current_page = target_page

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

    async def editdeck(self, army_type: str, heros: List[str], skills: List[List[str]]):
        # 유효성 검사
        assert len(heros) == 3, "hero는 보통 3명이여야 합니다." # 예외가 있겠지만, 일단 3명으로 만들자.
        assert len(skills) == 3, "hero 3이어야 합니다."
        for i in range(3):
            assert len(skills[i]) == 2, "각각의 skills는 2개의 전법을 가져야합니다"

        # path_find
        await self.navigate('DeckEditPage')
        await self.page.deck_configuration(self.pw.page, army_type, heros, skills)
        

simulator = Simulator()

async def crawl_website(content: str) -> str:
    async with async_playwright() as p:
        await simulator.start_browser(p)

        id: str = '01011111111'
        password: str = '1111'
        await simulator.login(id, password)
        await simulator.language("한국어")
        await simulator.season('2')
        await simulator.editdeck('방패병', ['유비', '관우', '장비'], [["함진영", "잠피기봉"], ["적진 함락","일망타진"], ["기세등등", "낙봉"]])

        crawled_content = await simulator.pw.page.content()
        await simulator.close_browser()

    return crawled_content[:100] + ' From UDP Server by python'