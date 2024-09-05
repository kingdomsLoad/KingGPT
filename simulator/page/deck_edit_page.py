from playwright.async_api import Page, Locator
from interface.Page import IPage
from typing import List
from simulator.page.deck_edit.team_setting import manage_team_setting
import asyncio

class DeckEditPage(IPage):
    async def navigate(self, page: Page, next_page: str):
        return await super().navigate(page, next_page)
    
    async def deck_configuration(self, page: Page, army_type: str, heros: List[str], skills: List[List[str]]):
        # 1. teamSetting 덱 설정
        #   ㄴ 군사시설 사기, 병사전, 협력, 병영, 군영 레벨 조정
        await manage_team_setting(page, True)
        # 2. del_btn 3개 장수 지우기 
        # 3. army-type 선택하기
        # 4. add_btn 3개 장수 추가하기
        # 5. add_skills
        return 'DeckEditPage'

    # 함수 사용 예시
    # await manage_team_setting(page, False)
