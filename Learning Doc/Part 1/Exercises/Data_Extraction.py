# Goal: Understand element selection

# Visit a news website  ==> https://www.nytimes.com/
# Extract all article headlines   ===> a p
# Save them to a list ===? []
# Print the count ===> print()

# Learning Point: You'll see how to work with multiple similar elements

import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = True)
        page = await browser.new_page()
        
        try:
            await page.goto("https://www.nytimes.com/", wait_until="networkidle", timeout=60000)        
        except:
            print("Network idle timeout - falling back to 'domcontentloaded")
            await page.goto("https://www.nytimes.com/", wait_until="domcontentloaded", timeout=60000)

        
        # await page.wait_for_selector("a p")

        
        headlines = await page.locator("a p").all_text_contents()
        
        # A set in Python does not allow duplicates — it keeps only unique values.
        cleaned = list({each.strip() for each in headlines if len(each.strip())>25})
        
        print(f"Total headlines {len(cleaned)}")
        for i, h in enumerate(cleaned, 1):
            print(f"{i}. {h}")
        
        await page.screenshot(path="Data_extraction_img/debug.png")
        await browser.close()
    
    
    
asyncio.run(main())