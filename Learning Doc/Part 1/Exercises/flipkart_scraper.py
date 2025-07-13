import asyncio
from playwright.async_api import async_playwright
import json
import re


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        scraped_Data = []
        url = "https://www.flipkart.com/search?q=headphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

        try:
            await page.goto(url)
            print("website loaded successfully")
        except Exception as e:
            print(f"Falied to load URL: {url}")
            print(f"Error: {str(e)}")
            await page.screenshot(path="Error_handle_img/debug.png")
            await browser.close()
            return

            
        products = page.locator("div[data-id]")
        
        for i in range(await products.count()):
            product = products.nth(i)
            
            title = await product.locator("a[title]").first.text_content() or "N/A"
            try:
                price = await product.locator('.Nx9bqj123').text_content() or "N/A"
            except:
                price = "N/A"
                price_divs = await product.locator("div").all_text_contents()
                for text in price_divs:
                    if "₹" in text:
                        match = re.match(r"₹\d[\d,]*", text.strip())
                        if match:
                            price = match.group(0)
                            break

            rating_locater = product.locator("span[id^='productRating'] div")
            rating = "N/A"
            if await rating_locater.count()>0:
                rating = await rating_locater.first.text_content()
            
            scraped_Data.append(
                {
                    "title": title.strip(),
                    "Price": price.strip(),
                    "rating": rating.strip()
                }
            )
        with open("flipkart_products.json", "w", encoding="utf-8") as f:
            json.dump(scraped_Data,f,indent=4,ensure_ascii=False)
            
        print(f"Scraped {len(scraped_Data)} Products")
        await browser.close()
            

        await browser.close()
    
    
asyncio.run(main())