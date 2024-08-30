from playwright.async_api import Page
from interface.Page import IPage
import re

class LoginPage(IPage):
    async def navigate(self, page: Page, next_page: str):
        return await super().navigate(page, next_page)

    async def login(self, page: Page, id: str, password: str):
        print("로그인 수행")
        # 등록 버튼 클릭
        await page.get_by_text("注册").nth(0).click()
        # 전화번호 입력란 클릭 및 입력
        phone_input = page.locator("uni-input").filter(has_text="手机号").get_by_role("textbox")
        await phone_input.click()
        await phone_input.fill(id)

        # 비밀번호 입력란 클릭 및 입력
        password_input = page.locator("uni-input").filter(has_text=re.compile(r"^密码$")).get_by_role("textbox")
        await password_input.fill(password)

        # 비밀번호 확인 입력란 클릭 및 입력
        repeat_password_input = page.locator("uni-input").filter(has_text="重复密码").get_by_role("textbox")
        await repeat_password_input.fill(password)

        # 이미지 클릭 (등록 확인 후 수행되는 것으로 보임)
        await page.get_by_text("注册").nth(1).click()

        # 일일 보상 수령
        await page.get_by_text("领取").nth(0).click()

        # 뒤로가기 버튼
        await page.locator(".back-btn").click()

        return 'MainPage'