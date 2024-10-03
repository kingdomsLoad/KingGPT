from playwright.async_api import Page, Locator
import asyncio
from typing import List

class Lineup:
    def __init__(self):
        self.page = None

    async def delete_heros(self, page: Page):
        btn_del = page.locator('uni-view.lineup-box > uni-view.hero-box > uni-view.army-row > uni-view.btn-del')
        
        count = await btn_del.count()
        
        for i in range(count):
            button = btn_del.nth(0)
            black_box_count = await page.locator('.blank-box').count()
            # print(f"black_box_count: {black_box_count}")

            # 버튼이 보이고 활성화되어 있는지 확인합니다
            if await button.is_visible() and await button.is_enabled():
                await button.click()
                # 클릭 후 잠시 대기합니다 (필요에 따라 조정)
                while True:
                    black_box_count_after = await page.locator('.blank-box').count()
                    if black_box_count_after > black_box_count:
                        break
                    await page.wait_for_timeout(100)

    async def add_heroes(self, page: Page, heroes: List[str]):
        btn_add_hero_locators = [page.locator('uni-view.lineup-box > uni-view.hero-box:nth-child({}) > uni-view.blank-box > uni-view.add-btn'.format(i)) for i in range(1, 4)]

        for i in range(0, 3):
            await btn_add_hero_locators[i].click()
            await page.wait_for_selector("//uni-view[contains(@class, 'hero-list')]", timeout=10000)

            element = page.locator(f"//uni-view[contains(@class, 'hero-name-box')][.//span[text()='{heroes[i]}']]",)
            await element.click()
            await page.wait_for_selector("//uni-view[contains(@class, 'hero-box-comp')]", timeout=10000)

    async def add_skills(self, page: Page, skills: List[List[str]]):
        skill_name_box_locators = [
            [page.locator(f'uni-view.hero-box:nth-child({i+1}) uni-view.skill-name-box').nth(j) for j in range(2)]
            for i in range(3)
            ]

        for hero_index in range(0, 3):
            for skill_index in range(0, 2):   
                await skill_name_box_locators[hero_index][skill_index].click()
                await page.wait_for_selector("uni-view.zf-popup", state="visible")

                skill_text = skills[hero_index][skill_index]

                # 전법 검색
                selectors = "uni-view.zf-popup input"
                await page.fill(selectors, skill_text)

                # 전법 클릭
                element = page.locator(f"uni-view.zf-btn:has(:text-is(\"{skill_text}\"))")
                await element.click()

                close_btn_selector = "uni-view.zf-popup uni-image.close-btn"
                await page.wait_for_selector(close_btn_selector, state="visible", timeout=500)
                close_btn = page.locator(close_btn_selector)
                await close_btn.click()
