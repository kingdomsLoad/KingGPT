from playwright.async_api import Page, Locator
import asyncio

class TeamSetting:
    async def configure(self, page: Page, target_state: bool):
        # 입장
        await self.click_right_arrow(page)

        # 만렙(default)으로 조정
        await self.check_and_set_button_state(page, target_state)

        # 퇴장
        await self.exit_team_settings(page)

        # 퇴장 확인
        await self.wait_for_lineup_box(page)

    async def click_right_arrow(self, page: Page):
        right_arrow = page.locator("uni-view.team-setting uni-image.right-arrow")
        await right_arrow.click()

    async def check_and_set_button_state(self, page: Page, target_state: bool):
        # 버튼 요소 선택
        assart_btn = await page.wait_for_selector("uni-view.btn.assart-btn")

        # 버튼의 초기 상태 확인
        initial_state = await self.get_button_state(assart_btn)
        print(f"초기 상태: {initial_state}")

        # 첫 번째 클릭 (상태 변경)
        await self.toggle_button(assart_btn)
        
        # 두 번째 클릭 (원래 상태로 돌아가거나 목표 상태로 설정)
        await self.toggle_button(assart_btn)

        # 버튼의 최종 상태 확인 및 목표 상태로 설정
        final_state = await self.get_button_state(assart_btn)
        if final_state != target_state:
            await self.toggle_button(assart_btn)
            print(f"최종 상태: {target_state}로 설정되었습니다.")
        else:
            print(f"이미 목표 상태: {target_state}입니다.")

    async def get_button_state(self, button: Locator) -> bool:
        return await button.evaluate("el => el.classList.contains('active')")

    async def toggle_button(self, button: Locator):
        initial_state = await self.get_button_state(button)
        await button.click()
        await self.wait_for_state_change(button, initial_state)

    async def wait_for_state_change(self, button: Locator, previous_state: bool):
        while True:
            current_state = await self.get_button_state(button)
            if current_state != previous_state:
                break
            await asyncio.sleep(0.1)  # 0.1초 대기 후 다시 확인

    async def exit_team_settings(self, page: Page):
        await page.locator(".back-btn").click()

    async def wait_for_lineup_box(self, page: Page):
        await page.wait_for_selector("uni-view.lineup-box", state="visible")