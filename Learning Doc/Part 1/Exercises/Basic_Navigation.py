import asyncio
from playwright.async_api import async_playwright


async def main():
    websites = {
    "flipkart":"https://www.flipkart.com/",
    "amazon":"https://www.amazon.in/"
}
    # This create a playwright instance that manage browsers
    async with async_playwright() as p:
        # launch Chrome browser (headless=False show the window)
        browser = await p.chromium.launch(headless=True)
        # think of this as opening new tab
        for website, url in websites.items():
            
            page = await browser.new_page()
            # Navigate to a typing URL and website (like typing and pressing enter )
            await page.goto(url, timeout = 60000)
            
            # take a screenshort (useful for debugging)
            await page.screenshot(path=f'Basic_nav_images/{website}.png')

            
            # close the browser
        await browser.close()
        




asyncio.run(main())