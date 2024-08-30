from playwright.async_api import Page
from interface.Page import IPage
import re

class MainPage(IPage):
    async def navigate(self, page: Page, next_page: str):
        return await super().navigate(page, next_page)
    
    async def change_language(self, page: Page, language: str):
        await page.get_by_text("简体中文").click()
        await page.get_by_text(language).click()
        await page.get_by_text("确认").click()

    async def change_season(self, page: Page, season: str):
        await page.get_by_text(re.compile("시즌")).click()
        if season == "1":
            await page.locator("uni-view.seasion-option-row").filter(has_text=re.compile(r"^시즌 1$")).click()
        if season == "2":
            await page.locator("uni-view.seasion-option-row").filter(has_text=re.compile(r"^시즌 2$")).click()
        if season == "3":
            await page.locator("uni-view.seasion-option-row").filter(has_text=re.compile(r"^시즌 3$")).click()
        if season == "pk":
            await page.locator("uni-view.seasion-option-row").filter(has_text=re.compile(r"^pk시즌$")).click()
            # 필요한 pk 시즌 누르는 버튼 추가해야함.
        await page.locator("uni-view").filter(has_text=re.compile(r"^확인$")).click()
