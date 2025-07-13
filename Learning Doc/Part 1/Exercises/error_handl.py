import asyncio
from playwright.async_api import async_playwright



async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        url = "https://www.thiswebsitedoesnotexist12345.com"

        try:
            await page.goto(url)
            print("website loaded successfully")
        except Exception as e:
            print(f"Falied to load URL: {url}")
            print(f"Error: {str(e)}")
            await page.screenshot(path="Error_handle_img/debug.png")
        await browser.close()
    
    
asyncio.run(main())