from playwright.async_api import Page, Locator
from interface.Page import IPage
from typing import List
from simulator.page.deck_edit.team_setting import TeamSetting
from simulator.page.deck_edit.lineup import Lineup
import asyncio

class DeckEditPage(IPage):
    def __init__(self):
        self.team_setting = TeamSetting()
        self.lineup = Lineup()

    async def navigate(self, page: Page, next_page: str):
        return await super().navigate(page, next_page)
    
    async def edit_deck(self, page: Page, army_type: str, heros: List[str], skills: List[List[str]]):
        # 1. teamSetting 덱 설정
        #   ㄴ 군사시설 사기, 병사전, 협력, 병영, 군영 레벨 조정
        await self.team_setting.configure(page, False)# True는 Target_bool이 참
        # 2. del_btn 3개 장수 지우기 
        await self.lineup.delete_heros(page)
        # 3. army-type 선택하기
        await self.lineup.select_army_type(page, army_type)
        # 4. add_btn 3개 장수 추가하기
        await self.lineup.add_heroes(page, heros)
        # 5. add_skills
        await self.lineup.add_skills(page, skills)
        return 'DeckEditPage'

    # 함수 사용 예시
    # await manage_team_setting(page, False)
