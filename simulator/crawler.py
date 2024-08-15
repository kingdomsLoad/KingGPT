from playwright.async_api import async_playwright

async def crawl_website(content: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('http://example.com')
        crawled_content = await page.content()
        await browser.close()

    return crawled_content[:100] + ' From UDP Server by python'