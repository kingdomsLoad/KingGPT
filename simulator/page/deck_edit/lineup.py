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

        try:
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
        except:
            return

    async def select_army_type(self, page: Page, army_type: str):
        """
        주어진 army_type에 해당하는 버튼을 클릭하고 선택이 완료될 때까지 대기합니다.
        :param page: Playwright Page 객체
        :param army_type: 선택할 군사 유형 (기병, 방패병, 궁병, 창병, 병기)
        """
        # 군사 유형과 해당 이미지 파일 매핑
        army_type_mapping = {
            "기병": "icon_qb@2x.png",
            "방패병": "icon_db@2x.png",
            "궁병": "icon_gb@2x.png",
            "창병": "icon_qiangb@2x.png",
            "병기": "icon_qx@2x.png"
        }

        # 입력된 army_type이 유효한지 확인
        if army_type not in army_type_mapping:
            raise ValueError(f"Unknown army_type: {army_type}. Valid types are: {', '.join(army_type_mapping.keys())}")

        # 해당 army_type의 이미지 파일명
        image_file = army_type_mapping[army_type]

        # 버튼의 img src를 기반으로 선택자 생성
        selector = f"img[src='/static/img/armyType/{image_file}']"

        # 버튼 요소 찾기
        button = page.locator(selector)

        # 버튼이 존재하는지 확인
        if not await button.count():
            raise Exception(f"Button for army_type '{army_type}' not found.")

        # 버튼 클릭
        await button.click()

        # 변경 사항이 반영될 때까지 대기
        # 예를 들어, 선택된 버튼에 'active' 클래스가 추가되거나 이미지가 변경되는 경우를 기다립니다.
        # 여기서는 이미지 파일명이 '_active'로 변경된다고 가정합니다.
        active_image_file = image_file.replace("@2x.png", "_active@2x.png")
        active_selector = f"img[src='/static/img/armyType/{active_image_file}']"

        try:
            await page.wait_for_selector(active_selector, timeout=5000)
            print(f"Successfully selected army type: {army_type}")
        except TimeoutError:
            raise TimeoutError(f"Timeout while waiting for army type '{army_type}' to be selected.")


        # await page.wait_for_selector(active_selector)

        # # for attempt in range(50):
        # #     count = await page.locator(active_selector).count()
        # #     if count == 1:
        # #         print(f"Successfully selected army type: {army_type}")
        # #         return
        # #     await asyncio.sleep(0.1)
        
        # raise TimeoutError(f"Timeout while waiting for army type '{army_type}' to be selected.")
