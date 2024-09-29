from playwright.async_api import Page, Locator
import asyncio

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
