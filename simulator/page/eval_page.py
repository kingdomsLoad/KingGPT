from playwright.async_api import Page
from interface.Page import IPage
from typing import List, Dict

class EvalPage(IPage):
    def __init__(self):
        self.data_plain_text = ""

    async def navigate(self, page: Page, next_page: str):
        return await super().navigate(page, next_page)

    async def eval(self, page: Page):
        data: Dict = await self.extract_all(page)
        self.data_plain_text = await self.format_data_as_string(data)
        return 'EvalPage'
    
    # async def eval_capture(self, page: Page):
    #     # await page.screenshot(path="screentshot.png", full_page=True)

    async def extract_heroes(self, page: Page) -> List[Dict]:
        heroes = []
        hero_boxes = page.locator("uni-view.hero-box")
        count = await hero_boxes.count()
        for i in range(count):
            hero = {}
            hero_box = hero_boxes.nth(i)
            
            # 장수 이름 추출
            hero_name = await hero_box.locator("uni-text.hero-name span").inner_text()
            hero['name'] = hero_name.strip()
            
            # 병종적성 추출
            type_box = hero_box.locator("uni-view.type-box")
            type_name = await type_box.locator("uni-text.type-name span").inner_text()
            hero['type'] = type_name.strip()
            
            # 스킬 추출
            skills = []
            skill_rows = hero_box.locator("uni-view.skill-name-row")
            skill_count = await skill_rows.count()
            for j in range(skill_count):
                skill_name = await skill_rows.nth(j).locator("uni-text.skill-name span").inner_text()
                skills.append(skill_name.strip())
            hero['skills'] = skills
            
            # 병서(bs) 추출
            bs_texts = await hero_box.locator("uni-view.bs-box uni-text.bs-text").all_inner_texts()
            bs = [text.strip() for text in bs_texts]
            hero['bs'] = bs
            
            # 스텟 추출
            stat_text = await hero_box.locator("uni-view.bs-box uni-text.bs-text.jd span").inner_text()
            stat = stat_text.strip()
            hero['stat'] = stat
            
            heroes.append(hero)
        return heroes

    async def extract_scores(self, page: Page) -> Dict:
        scores = {}
        try:
            # pvp 점수 추출
            # 'uni-text.score-title.pvp' 요소 바로 다음에 있는 'uni-view.score-box uni-text.score span' 요소를 선택
            pvp_score_locator = page.locator("uni-text.score-title.pvp + uni-view.score-box uni-text.score span")
            pvp_score_text = await pvp_score_locator.inner_text()
            scores['pvp'] = float(pvp_score_text.strip())

            # pve 점수 추출
            # 'uni-text.score-title.pve' 요소 바로 다음에 있는 'uni-view.score-box uni-text.score span' 요소를 선택
            pve_score_locator = page.locator("uni-text.score-title.pve + uni-view.score-box uni-text.score span")
            pve_score_text = await pve_score_locator.inner_text()
            scores['pve'] = float(pve_score_text.strip())
        except Exception as e:
            print(f"점수 추출 중 오류 발생: {e}")
            scores['pvp'] = None
            scores['pve'] = None
        return scores

    async def extract_restrictions(self, page: Page) -> Dict:
        restrictions = {}
        try:
            # item-row 내의 item-box 개수 세기
            item_row = page.locator("uni-view.restraint-box > uni-view.item-row")
            item_boxes = item_row.locator("uni-view.item-box")
            item_count = await item_boxes.count()

            items = {}
            for i in range(item_count):
                item_box = item_boxes.nth(i)
                
                # item-name과 item-num을 명확하게 구분해서 추출
                item_name_span = item_box.locator("uni-text.item-name > span:first-child")
                item_num_span = item_box.locator("uni-text.item-num > span")

                item_name = await item_name_span.inner_text()
                item_num = await item_num_span.inner_text()
                item_name = item_name.replace(item_num, '')

                # item_name과 item_num을 바로 items에 추가
                items[item_name.strip()] = float(item_num.strip())

            restrictions['items'] = items
        except Exception as e:
            print(f"아이템 추출 중 오류 발생: {e}")
            restrictions['items'] = {}
        return restrictions

    async def extract_all(self, page: Page) -> Dict:
        data = {}
        data['heroes'] = await self.extract_heroes(page)
        data['scores'] = await self.extract_scores(page)
        data['restrictions'] = await self.extract_restrictions(page)
        return data

    async def format_data_as_string(self, data) -> str:
        lines = []

        # 1. Header: 방SAS
        army_types = [hero['type'] for hero in data['heroes']]
        # '방S', '방A', '방S' → '방SAS'
        # assuming all types start with '방'
        army_suffixes = [atype.replace('방', '') for atype in army_types]
        header = '방' + ''.join(army_suffixes)
        lines.append(header)

        # 2. Hero 정보
        for hero in data['heroes']:
            name = hero['name']
            skills = ' '.join(hero['skills'])
            # 병서는 마지막 항목이 스텟이므로 제외하고 공백 제거
            bs = ' '.join([bs_item.replace(' ', '') for bs_item in hero['bs'][:-1]])
            stat = hero['bs'][-1]
            hero_line = f"{name} {skills} | {bs} {stat}"
            lines.append(hero_line)

        # 3. 빈 줄 추가
        lines.append('')

        # 4. 점수 정보
        scores = data['scores']
        lines.append(f"pvp {scores['pvp']}")
        lines.append(f"pve {scores['pve']}")
        lines.append('')

        # 5. 억제관계 정보
        restrictions = data['restrictions']
        for item, value in restrictions['items'].items():
            lines.append(f"{item} {value}")

        # 6. 전체 데이터 문자열로 결합
        return "\n".join(lines)

