import asyncio
from playwright.async_api import async_playwright

"""Render cv.html to assets/files/marcus-fogg-cv.pdf.

Serve the site first: python3 -m http.server 8000
"""

OUT = "assets/files/marcus-fogg-cv.pdf"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("http://localhost:8000/cv.html", wait_until="networkidle")
        await pg.wait_for_timeout(500)
        await pg.emulate_media(media="print")
        await pg.pdf(path=OUT, format="A4", print_background=True,
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        print("written to", OUT, "| console errors:", errs or "none")
        await b.close()

asyncio.run(main())
