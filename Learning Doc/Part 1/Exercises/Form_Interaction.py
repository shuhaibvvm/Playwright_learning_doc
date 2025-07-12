# Exercise 2: Form Interaction (10 minutes)
# Goal: Understand user simulation

# Go to a search engine
# Fill in a search query
# Submit the form
# Wait for results to load

import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = False)  
        page = await browser.new_page()
        
        await page.goto("https://www.amazon.in/", timeout =60000) # , wait_until='networkidle'
        
        input_box = page.locator("input[type = 'text']")
        await input_box.type("smartphone",delay = 100)
        
        await input_box.press("Enter")
        
        # await page.wait_for_selector("h2") 
        await page.wait_for_selector('[role="listitem"]')


        
        await page.screenshot(path="form_interation_img/page.png")
        
        await browser.close()


asyncio.run(main())        
        

