from abc import ABC, abstractmethod
from playwright.async_api import Page

class IPage(ABC):
    @abstractmethod
    async def navigate(self, page: Page, next_page: str):
        pass