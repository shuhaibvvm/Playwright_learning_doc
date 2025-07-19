import asyncio
from playwright.async_api import async_playwright
from capsolver import CapSolver

CAPSOLVER_API_KEY = "YOUR_CAPSOLVER_API_KEY"  # Replace this
TARGET_URL = "https://www.google.com/recaptcha/api2/demo"  # Demo page
SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"  # Public demo sitekey

async def solve_captcha():
    capsolver = CapSolver(api_key=CAPSOLVER_API_KEY)

    print("[*] Solving CAPTCHA...")
    solution = capsolver.solve({
        "type": "ReCaptchaV2TaskProxyless",
        "websiteURL": TARGET_URL,
        "websiteKey": SITE_KEY
    })

    print("[+] CAPTCHA Solved!")
    return solution['gRecaptchaResponse']

async def main():
    captcha_token = await solve_captcha()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(TARGET_URL)

        # Inject the token into the page
        await page.evaluate(f'''
        document.getElementById("g-recaptcha-response").innerHTML = "{captcha_token}";
        ''')

        # Trigger submit by clicking or JS
        await page.click("#recaptcha-demo-submit")  # for demo site
        await asyncio.sleep(5)  # wait for result

        await browser.close()

asyncio.run(main())
