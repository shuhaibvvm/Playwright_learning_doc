import asyncio
import random
import json
from playwright.async_api import async_playwright
from datetime import datetime

class AdvancedStealthScraper:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        self.screen_resolutions = [
            {'width': 1920, 'height': 1080},
            {'width': 1366, 'height': 768},
            {'width': 1440, 'height': 900},
            {'width': 1536, 'height': 864}
        ]
    
    async def create_stealth_browser(self):
        """Creates a browser with advanced anti-detection"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-dev-shm-usage',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-extensions-file-access-check',
                    '--disable-extensions-http-throttling',
                    '--disable-ipc-flooding-protection',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--force-color-profile=srgb',
                    '--disable-component-extensions-with-background-pages'
                ]
            )
            
            resolution = random.choice(self.screen_resolutions)
            context = await browser.new_context(
                user_agent=random.choice(self.user_agents),
                viewport=resolution,
                device_scale_factor=1,
                has_touch=False,
                is_mobile=False,
                locale='en-US',
                timezone_id='America/New_York',
                extra_http_headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Cache-Control': 'max-age=0',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1'
                }
            )
            
            # Advanced JavaScript injection to hide automation
            await context.add_init_script("""
                // Remove webdriver property
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                    configurable: true
                });
                
                // Mock plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => ({
                        length: 5,
                        0: { name: 'Chrome PDF Plugin' },
                        1: { name: 'Chromium PDF Plugin' },
                        2: { name: 'Microsoft Edge PDF Plugin' },
                        3: { name: 'PDF Viewer' },
                        4: { name: 'Chrome PDF Viewer' }
                    }),
                    configurable: true
                });
                
                // Mock languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                    configurable: true
                });
                
                // Mock permissions
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
                
                // Override chrome runtime
                if (window.chrome && window.chrome.runtime) {
                    Object.defineProperty(window.chrome, 'runtime', {
                        get: () => undefined,
                        configurable: true
                    });
                }
                
                // Mock hardware concurrency
                Object.defineProperty(navigator, 'hardwareConcurrency', {
                    get: () => 4 + Math.floor(Math.random() * 4),
                    configurable: true
                });
                
                // Mock memory (if available)
                if ('deviceMemory' in navigator) {
                    Object.defineProperty(navigator, 'deviceMemory', {
                        get: () => [2, 4, 8][Math.floor(Math.random() * 3)],
                        configurable: true
                    });
                }
                
                // Mock connection
                Object.defineProperty(navigator, 'connection', {
                    get: () => ({
                        downlink: 10,
                        effectiveType: '4g',
                        rtt: 100
                    }),
                    configurable: true
                });
                
                // Override automation detection methods
                window.outerHeight = window.screen.height;
                window.outerWidth = window.screen.width;
                
                // Mock getBattery if available
                if (navigator.getBattery) {
                    const originalGetBattery = navigator.getBattery;
                    navigator.getBattery = () => Promise.resolve({
                        charging: true,
                        level: 0.8 + Math.random() * 0.2,
                        chargingTime: Infinity,
                        dischargingTime: 7200
                    });
                }
                
                // Hide automation in iframes
                Object.defineProperty(HTMLIFrameElement.prototype, 'contentWindow', {
                    get: function() {
                        return window;
                    }
                });
                
                // Mock canvas fingerprinting protection
                const getContext = HTMLCanvasElement.prototype.getContext;
                HTMLCanvasElement.prototype.getContext = function(type) {
                    const context = getContext.apply(this, arguments);
                    if (type === '2d') {
                        const originalFillText = context.fillText;
                        context.fillText = function() {
                            // Add slight randomization to text rendering
                            const noise = Math.random() * 0.01;
                            arguments[1] += noise;
                            arguments[2] += noise;
                            return originalFillText.apply(this, arguments);
                        };
                    }
                    return context;
                };
                
                // Mock WebGL fingerprinting protection
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === 37445) { // UNMASKED_VENDOR_WEBGL
                        return 'Intel Inc.';
                    }
                    if (parameter === 37446) { // UNMASKED_RENDERER_WEBGL
                        return 'Intel Iris OpenGL Engine';
                    }
                    return getParameter.apply(this, arguments);
                };
                
                // Mock audio context fingerprinting
                if (window.AudioContext || window.webkitAudioContext) {
                    const OriginalAudioContext = window.AudioContext || window.webkitAudioContext;
                    const audioCtx = new OriginalAudioContext();
                    const originalCreateOscillator = audioCtx.createOscillator;
                    audioCtx.createOscillator = function() {
                        const oscillator = originalCreateOscillator.apply(this, arguments);
                        const originalStart = oscillator.start;
                        oscillator.start = function() {
                            // Add micro-timing variations
                            if (arguments.length > 0) {
                                arguments[0] += Math.random() * 0.001;
                            }
                            return originalStart.apply(this, arguments);
                        };
                        return oscillator;
                    };
                }
                
                // Hide Selenium/WebDriver traces
                delete window.webdriver;
                delete window._Selenium_IDE_Recorder;
                delete window._selenium;
                delete window.__selenium_recorder;
                delete window.__selenium_evaluate;
                delete window.__selenium_record;
                delete window.__fxdriver_id;
                delete window.__fxdriver_unwrapped;
                delete window.__driver_evaluate;
                delete window.__webdriver_evaluate;
                delete window.__driver_unwrapped;
                delete window.__webdriver_unwrapped;
                delete window.__fxdriver_evaluate;
                delete window.__nightmare;
                delete window.nightmare;
                delete window.phantomjs;
                delete window.callSelenium;
                delete window.callPhantom;
                delete window._phantom;
                
                // Mock timing functions to appear more human
                const originalSetTimeout = window.setTimeout;
                window.setTimeout = function(fn, delay) {
                    const humanDelay = delay + Math.random() * 50; // Add 0-50ms variance
                    return originalSetTimeout(fn, humanDelay);
                };
                
                // Add mouse movement noise
                let lastMouseMove = Date.now();
                const originalAddEventListener = Element.prototype.addEventListener;
                Element.prototype.addEventListener = function(type, listener, options) {
                    if (type === 'mousemove') {
                        const humanListener = function(e) {
                            const now = Date.now();
                            if (now - lastMouseMove > 16) { // Throttle to ~60fps
                                lastMouseMove = now;
                                return listener.apply(this, arguments);
                            }
                        };
                        return originalAddEventListener.call(this, type, humanListener, options);
                    }
                    return originalAddEventListener.call(this, type, listener, options);
                };
            """)
            
            return browser, context
    
    async def human_delay(self, min_ms=500, max_ms=2000):
        """Enhanced human-like delay with variance"""
        base_delay = random.uniform(min_ms, max_ms) / 1000
        # Add occasional longer pauses (like humans reading)
        if random.random() < 0.1:  # 10% chance
            base_delay *= 2
        await asyncio.sleep(base_delay)
    
    async def simulate_human_browsing(self, page):
        """Simulate realistic human browsing behavior"""
        # Random mouse movements
        for _ in range(random.randint(2, 5)):
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            await page.mouse.move(x, y)
            await asyncio.sleep(random.uniform(0.1, 0.3))
        
        # Realistic scrolling patterns
        scroll_patterns = [
            # Quick scroll down
            lambda: page.mouse.wheel(0, random.randint(200, 500)),
            # Slow scroll down
            lambda: page.mouse.wheel(0, random.randint(50, 150)),
            # Scroll up (like re-reading)
            lambda: page.mouse.wheel(0, -random.randint(100, 300)),
        ]
        
        for _ in range(random.randint(3, 6)):
            pattern = random.choice(scroll_patterns)
            await pattern()
            await self.human_delay(300, 800)
        
        # Sometimes hover over elements
        if random.random() < 0.7:  # 70% chance
            try:
                elements = await page.query_selector_all('a, button, .clickable')
                if elements:
                    element = random.choice(elements)
                    await element.hover()
                    await self.human_delay(500, 1500)
            except:
                pass  # Ignore if elements not found
    
    async def bypass_bot_detection(self, page):
        """Additional bot detection bypass techniques"""
        # Check for common bot detection scripts
        scripts = await page.query_selector_all('script')
        for script in scripts:
            try:
                src = await script.get_attribute('src')
                if src and any(detector in src for detector in ['recaptcha', 'cloudflare', 'imperva', 'distil']):
                    print(f"Detected bot protection script: {src}")
                    # Add extra delay and human behavior
                    await self.simulate_human_browsing(page)
                    await self.human_delay(3000, 7000)
            except:
                continue
        
        # Check for hidden bot detection elements
        try:
            hidden_elements = await page.query_selector_all('[style*="display: none"], [style*="visibility: hidden"]')
            if len(hidden_elements) > 10:  # Suspicious number of hidden elements
                await self.simulate_human_browsing(page)
                await self.human_delay(2000, 4000)
        except:
            pass
    
    async def scrape_with_stealth(self, url, max_retries=3):
        """Enhanced scraping with retry logic and stealth"""
        for attempt in range(max_retries):
            try:
                async with async_playwright() as p:
                    browser, context = await self.create_stealth_browser()
                    page = await context.new_page()
                    
                    # Set up request interception for additional stealth
                    await page.route('**/*', lambda route: route.continue_())
                    
                    try:
                        # Navigate with realistic timing
                        await page.goto(url, wait_until='networkidle', timeout=30000)
                        await self.human_delay(2000, 5000)
                        
                        # Check for and bypass bot detection
                        await self.bypass_bot_detection(page)
                        
                        # Simulate human browsing
                        await self.simulate_human_browsing(page)
                        
                        # Wait for content and extract data
                        data = await self.extract_data(page)
                        
                        # Final human delay before closing
                        await self.human_delay(1000, 3000)
                        
                        if data:
                            return data
                        else:
                            print(f"No data extracted, attempt {attempt + 1}/{max_retries}")
                            
                    except Exception as e:
                        print(f"Error during scraping attempt {attempt + 1}: {e}")
                        if attempt == max_retries - 1:
                            raise
                    finally:
                        await browser.close()
                        
            except Exception as e:
                print(f"Browser setup error attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(random.uniform(5, 10))  # Wait before retry
                else:
                    return None
        
        return None
    
    async def test_bot_detection(self, page):
        """Test if your setup is detected as a bot"""
        test_sites = [
            "https://bot.sannysoft.com/",      # Comprehensive bot detection
            "https://pixelscan.net/",          # Fingerprint analysis
            "https://www.whatismybrowser.com/" # Browser info
        ]
        
        results = {}
        
        for site in test_sites:
            print(f"\nTesting: {site}")
            try:
                await page.goto(site, wait_until='networkidle', timeout=30000)
                await self.human_delay(3000, 6000)
                
                # Take screenshot for manual inspection
                site_name = site.split("/")[2].replace(".", "_")
                await page.screenshot(path=f'test_{site_name}.png')
                
                # Check for common bot detection indicators
                page_content = await page.content()
                bot_indicators = [
                    'webdriver', 'selenium', 'phantomjs', 'nightmare',
                    'bot detected', 'automation', 'headless'
                ]
                
                detected = any(indicator.lower() in page_content.lower() 
                             for indicator in bot_indicators)
                
                if detected:
                    print(f"❌ Bot detection possible - check screenshot")
                    results[site] = "DETECTED"
                else:
                    print(f"✅ Passed - No obvious detection")
                    results[site] = "PASSED"
                    
                await self.human_delay(2000, 4000)
                
            except Exception as e:
                print(f"❌ Failed to load - {e}")
                results[site] = f"ERROR: {e}"
        
        return results
    
    async def run_detection_test(self):
        """Run bot detection tests with current configuration"""
        print("🔍 Testing bot detection with current stealth setup...")
        
        async with async_playwright() as p:
            browser, context = await self.create_stealth_browser()
            page = await context.new_page()
            
            try:
                results = await self.test_bot_detection(page)
                
                print("\n" + "="*50)
                print("BOT DETECTION TEST RESULTS")
                print("="*50)
                for site, result in results.items():
                    status_icon = "✅" if result == "PASSED" else "❌"
                    print(f"{status_icon} {site}: {result}")
                print("="*50)
                
                return results
                
            finally:
                await browser.close()

    async def extract_data(self, page):
        """Enhanced data extraction with multiple fallbacks"""
        try:
            # Wait for page to be fully loaded
            await page.wait_for_load_state('networkidle', timeout=15000)
            
            # Try multiple selectors for each piece of data
            title_selectors = ['h1', '.title', '[data-testid="title"]', '.product-title', '.heading']
            price_selectors = ['.price', '.a-price-whole', '.cost', '[data-testid="price"]', '.amount']
            rating_selectors = ['.rating', '.a-icon-alt', '.stars', '[data-testid="rating"]', '.score']
            
            data = {'scraped_at': datetime.now().isoformat()}
            
            # Extract title
            for selector in title_selectors:
                try:
                    element = await page.wait_for_selector(selector, timeout=3000)
                    if element:
                        data['title'] = (await element.text_content()).strip()
                        break
                except:
                    continue
            
            # Extract price
            for selector in price_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        price_text = (await element.text_content()).strip()
                        if price_text:
                            data['price'] = price_text
                            break
                except:
                    continue
            
            # Extract rating
            for selector in rating_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        rating_text = (await element.text_content()).strip()
                        if rating_text:
                            data['rating'] = rating_text
                            break
                except:
                    continue
            
            # Get page metadata
            try:
                data['url'] = page.url
                data['title'] = data.get('title', await page.title())
                data['meta_description'] = await page.get_attribute('meta[name="description"]', 'content') or 'N/A'
            except:
                pass
            
            # Ensure we got something useful
            if len([v for v in data.values() if v and v != 'N/A']) > 1:
                return data
            else:
                return None
                
        except Exception as e:
            print(f"Error extracting data: {e}")
            return None

# Usage example with error handling and bot detection testing
async def main():
    scraper = AdvancedStealthScraper()
    
    # First, test if our stealth setup is working
    print("🧪 Running bot detection tests first...")
    test_results = await scraper.run_detection_test()
    
    # Check if we passed most tests
    passed_tests = sum(1 for result in test_results.values() if result == "PASSED")
    total_tests = len(test_results)
    
    if passed_tests < total_tests * 0.6:  # Less than 60% passed
        print("⚠️  Warning: Bot detection tests show potential issues!")
        print("Consider reviewing the stealth configuration.")
    else:
        print("✅ Stealth setup looks good! Proceeding with scraping...")
    
    # Proceed with actual scraping
    urls = [
        "https://example-store.com/product/123",
        "https://another-site.com/item/456"
    ]
    
    results = []
    for url in urls:
        print(f"\n🔍 Scraping: {url}")
        data = await scraper.scrape_with_stealth(url)
        if data:
            results.append(data)
            print(f"✅ Success: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Failed to scrape: {url}")
        
        # Delay between requests (random 10-20 seconds)
        delay = random.uniform(10, 20)
        print(f"⏱️  Waiting {delay:.1f}s before next request...")
        await asyncio.sleep(delay)
    
    print(f"\n📊 Summary: Successfully scraped {len(results)}/{len(urls)} URLs")
    return results

async def test_only():
    """Run only bot detection tests without scraping"""
    scraper = AdvancedStealthScraper()
    return await scraper.run_detection_test()

if __name__ == "__main__":
    # Uncomment the line you want to run:
    results = asyncio.run(main())          # Full scraping with tests
    # results = asyncio.run(test_only())   # Only run bot detection tests