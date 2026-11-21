"""Render scripts/og-card.html to assets/img/og-marcus-fogg.jpg at 1200x630.

That's the image LinkedIn, Slack and the rest show when the site is shared.
Rerun it whenever the card or the headshot changes.

Serve the site first: python3 -m http.server 8000
"""

import asyncio
from playwright.async_api import async_playwright

OUT = "assets/img/og-marcus-fogg.jpg"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1200, "height": 630},
                                      device_scale_factor=1)
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto("http://localhost:8000/scripts/og-card.html",
                        wait_until="networkidle")
        await page.wait_for_timeout(400)          # let the webfonts settle
        await page.screenshot(path=OUT, type="jpeg", quality=88)
        print("written to", OUT, "| console errors:", errors or "none")
        await browser.close()


asyncio.run(main())
