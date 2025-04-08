from playwright.async_api import async_playwright

async def fetch_with_playwright(url):
    async def _get_content():
        try:
            async with async_playwright() as p:
                headless_mode = False if "nykaafashion" in url else True
                browser = await p.chromium.launch(headless=headless_mode, args=["--headless=new"])
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                    viewport={"width": 1280, "height": 800},
                    locale='en-US',
                )
                page = await context.new_page()
                await page.goto(url, timeout=30000)

                try:
                    await page.wait_for_selector("text='Add to Bag'", timeout=6000)
                except:
                    pass

                content = await page.content()
                await browser.close()
                return content
        except Exception as e:
            print(f"⚠️ Playwright fetch error: {e}")
            return None

    try:
        return await _get_content()
    except Exception as e:
        print(f"⚠️ Error in fetch_with_playwright: {e}")
        return None
