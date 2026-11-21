"""Render the live page and shoot the bits that are hard to judge from source.

Serve the site first: python3 -m http.server 8000
Output lands in /tmp/check/.
"""

import asyncio
import os
from playwright.async_api import async_playwright

OUT = "/tmp/check"


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1340, "height": 900},
                                      device_scale_factor=2)
        errors, failed = [], []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("requestfailed", lambda r: failed.append(r.url))

        await page.goto("http://localhost:8000/", wait_until="networkidle")
        await page.wait_for_timeout(600)

        # Park the pointer in the top-left and put it back there after every
        # hover. Chromium recomputes :hover when the page scrolls, so a pointer
        # left mid-screen silently hovers whatever scrolls under it and the
        # "resting" shots come out in their hover state.
        async def rest():
            await page.mouse.move(4, 4)
            await page.wait_for_timeout(600)

        await rest()

        # Scroll the whole page so every observer fires, then come back.
        await page.evaluate("""() => new Promise(done => {
            let y = 0;
            const step = () => {
                y += 420;
                window.scrollTo(0, y);
                if (y < document.body.scrollHeight) setTimeout(step, 90);
                else setTimeout(done, 2500);
            };
            step();
        })""")

        # Did the figures land on their authored values after counting?
        figures = await page.eval_on_selector_all(
            ".stat__figure, .proof__figure", "els => els.map(e => e.textContent.trim())")

        # Did the icon strokes get released?
        offsets = await page.eval_on_selector_all(
            ".pillar__icon > *",
            "els => els.map(e => e.style.strokeDashoffset || e.style.opacity || '-')")

        await page.evaluate("window.scrollTo(0, 0)")
        await rest()
        await page.screenshot(path=f"{OUT}/full.png", full_page=True)

        # The in-house card, resting.
        await page.locator(".case--feature").scroll_into_view_if_needed()
        await page.wait_for_timeout(400)
        await rest()
        await page.locator(".case--feature").screenshot(path=f"{OUT}/feature.png")

        # The same card with the logo plaque and colours up.
        await page.locator(".case--feature .case__logo a").hover()
        await page.wait_for_timeout(700)
        await page.locator(".case--feature").screenshot(path=f"{OUT}/feature-hover.png")

        # A compact card hovered, to check the darkest logos read on the plaque.
        await page.locator(".case--compact").nth(2).hover()
        await page.wait_for_timeout(700)
        await page.locator(".work__grid--compact").screenshot(path=f"{OUT}/compact-hover.png")

        # Employer row: resting, then one logo in colour.
        await page.locator(".employers").scroll_into_view_if_needed()
        await page.wait_for_timeout(300)
        await rest()
        await page.locator(".employers").screenshot(path=f"{OUT}/employers.png")
        # The track never stops on its own, so Playwright would wait forever for
        # a stable box. Pausing it is what a real hover does to it anyway.
        await page.evaluate("document.querySelector('.marquee__track').style.animationPlayState = 'paused'")
        await page.wait_for_timeout(200)
        await page.locator(".marquee__set").first.locator("li").nth(2).hover()
        await page.wait_for_timeout(700)
        await page.locator(".employers").screenshot(path=f"{OUT}/employers-hover.png")

        # Workshop photo, grey then colour.
        await page.locator(".about__photo").scroll_into_view_if_needed()
        await page.wait_for_timeout(300)
        await rest()
        await page.locator(".about__photo").screenshot(path=f"{OUT}/photo.png")
        await page.locator(".about__photo").hover()
        await page.wait_for_timeout(800)
        await page.locator(".about__photo").screenshot(path=f"{OUT}/photo-hover.png")

        print("figures:", figures)
        print("icon shapes released:", offsets)
        print("console errors:", errors or "none")
        print("failed requests:", failed or "none")
        await browser.close()


asyncio.run(main())
