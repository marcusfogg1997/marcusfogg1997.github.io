# marcusfogg.com

Single-page personal portfolio site. Plain HTML and CSS, no build step and no
framework. Open `index.html` in a browser and it works.

The header links are anchors to sections on the one page: Work, About, Approach,
Contact. The only JavaScript is fifteen lines at the bottom of `index.html` that
underline whichever nav item is in view. Turn JavaScript off and the nav still
works, it just stops highlighting.

## What's in here

```
index.html                       the homepage
cv.html                          the CV, also the source for the PDF
robots.txt, sitemap.xml          for search engines and AI crawlers
assets/css/styles.css            all styling, design tokens at the top
assets/fonts/                    Cormorant + Instrument Sans (self-hosted .woff2)
assets/img/                      portrait at 3 sizes, WebP + JPEG, plus favicon
assets/img/logos/                client and employer logos, one colour file each
assets/img/og-marcus-fogg.jpg    the image shown when the site is shared
assets/files/marcus-fogg-cv.pdf  the CV the site links to
originals/                       the colour logo files the above are built from
scripts/                         build and check scripts, not served
```

Design tokens (colours, type scale, spacing) are CSS custom properties in the
`:root` block at the top of `styles.css`. Change a colour there and it updates
everywhere.

| Token | Value | Used for |
| --- | --- | --- |
| `--cream` | `#f8f7f3` | page background |
| `--ink` | `#131711` | body text, solid button |
| `--ink-deep` | `#101610` | Selected Work section |
| `--green` | `#0b5031` | accent, italics, Contact section |
| `--mist` | `#edf4ee` | How I Work section |
| `--muted` | `#62675f` | secondary text |
| `--on-dark` | `#c1cbbf` | secondary text on dark backgrounds |

## Previewing it locally

Double-clicking `index.html` mostly works, but browsers block web fonts over
`file://`. To see it exactly as visitors will:

```bash
cd marcus-fogg-site
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Putting it on GitHub Pages

You'll need a GitHub account first. Sign up at <https://github.com/signup>.
It's free and Pages hosting is free with it.

**1. Create the repository**

On GitHub, click **New repository**. Name it `marcusfogg.github.io`
(substituting your username). Set it to **Public**, because Pages needs that on the
free plan. Don't tick "Add a README", you already have one.

**2. Upload the files**

Easiest route, no command line: on the empty repo page click
**uploading an existing file**, then drag in everything from this folder,
including the `assets` folder. Commit.

If you'd rather use the terminal:

```bash
cd marcus-fogg-site
git init
git add .
git commit -m "Initial site"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/marcusfogg.github.io.git
git push -u origin main
```

**3. Turn on Pages**

In the repo, go to **Settings → Pages**. Under "Build and deployment", set
Source to **Deploy from a branch**, branch `main`, folder `/ (root)`. Save.

Give it a minute, then your site is live at
`https://YOUR-USERNAME.github.io`.

**4. Custom domain (optional)**

If you buy `marcusfogg.com`, add it under **Settings → Pages → Custom domain**,
then at your registrar point the DNS at GitHub:

- Four `A` records for the apex domain: `185.199.108.153`, `185.199.109.153`,
  `185.199.110.153`, `185.199.111.153`
- One `CNAME` record for `www` pointing at `YOUR-USERNAME.github.io`

Tick **Enforce HTTPS** once the certificate has been issued. Also update the
`<link rel="canonical">` and `og:image` URLs in `index.html` to the real domain.

## Contact

There's no form. The Contact section is a mailto button and a LinkedIn link,
so there's no third-party form service to sign up for, pay for or maintain,
and nothing to break silently.

If you ever want a form back, Formspree is the usual route for a static site:
sign up, create a form, and point a `<form action="...">` at the endpoint it
gives you.

## The CV

`cv.html` is the CV, styled from the same tokens as the site. It's a real page,
so it works at `/cv.html` as well as being the source of the PDF.

`assets/files/marcus-fogg-cv.pdf` is generated from it:

```bash
python3 -m http.server 8000          # in one terminal
python3 scripts/cv-to-pdf.py         # in another
```

Edit `cv.html`, regenerate, and both the web version and the download stay in
step. The print rules live at the bottom of `assets/css/cv.css`, and one trick
there is load-bearing:

```css
@page { margin: 0; }            /* so the cream reaches the paper edge */
.cv {
  padding: 11mm 14mm;           /* the real margin, kept off the edge */
  background: var(--cream);
  box-decoration-break: clone;  /* repeats both on every page */
}
```

Without `box-decoration-break: clone`, the padding and background are drawn
once across the whole box, so page one gets a margin and page two starts hard
against the paper edge. With it, each page fragment redraws both. Setting the
margin on `@page` instead would fix the spacing but leave white strips at the
edges, which defeats the point.

It's tuned to land on two pages, so adding several bullets will push it to
three. Check before you send it.

## Swapping an older CV PDF

Replace `assets/files/marcus-fogg-cv.pdf` with the new file, keeping the same
filename, and both links on the page pick it up. Nothing else to change.

## Logos

`assets/img/logos/` holds one file per brand, made from the colour originals by
`scripts/logos.py`: the background is knocked out to transparent and the
artwork keeps its own colours.

That single file covers all three states the site needs, using a CSS filter:

| Where | Filter | Looks like |
| --- | --- | --- |
| Where I've worked row | `brightness(0) opacity(.58)` | ink |
| Selected Work cards | `brightness(0) invert(1) opacity(.92)` | white |
| either, on hover | `none` | the real brand colours |

`brightness(0)` multiplies every colour channel by zero without touching the
alpha, so the artwork collapses to a flat silhouette with its holes intact.
That's why there's no second set of mono files to keep in step.

It's a knockout rather than a flatten, which is why Crown's crown, Homeflow's
chevron, Famly's heart and Reload's arrow still read as shapes. They're cut out
of the mark rather than drawn on top of it.

The script quantises each PNG with `pngquant` if it's installed
(`pip install pngquant-cli`). Flat-colour artwork loses nothing visible and the
files come down by about two thirds. Without it the logos still build, just
heavier.

On the dark Selected Work cards, hovering a card fades a cream plaque in behind
the logo before revealing its colours. Every one of these marks is drawn for a
light background, and most of them are near-black: Ami and Startle would be
invisible against the card without something to sit on.

The script flattens each source onto white before it does anything else. Some
logos arrive on a transparent background, and skipping that step makes the
script read the background as black: dark wordmarks then score as nearly
background and come out half transparent, while white knockouts score as ink
and fill in solid. If a converted logo looks washed out or has lost a shape
from inside its mark, that's the first thing to check.

Each logo sits inside the `<h3 class="case__logo">` at the top of its card, so
the logo is the card's heading. The client name lives in the image's `alt`,
which is what a screen reader announces for that heading.

Each one carries an inline `--s` value. That's an optical size multiplier, not
a bug. Crown is a two-line lockup and StoreFeeder is a bare wordmark, so
matching their pixel heights would make one look tiny and the other enormous.
The multipliers make the wordmarks read at the same size.

To add or replace one, drop the colour original into `originals/`, add a line
to `SOURCES` in `scripts/logos.py`, run it, then set an `--s` value on the new
image, eyeballed against the others in its row.

`originals/` holds the colour source files. Nothing on the site links to them,
so they add nothing to page weight, but keeping them means the logos can be
regenerated without hunting the files down again.

A logo with a gradient or a photographic element knocks out muddily. If a
client's brand kit has an official reversed or mono version, use that instead
of converting the colour one.

## Motion

All of it is decoration layered on top of a page that's already complete. The
figures are in the HTML, the icons render on their own, and the script bails
out entirely for anyone whose system asks for reduced motion. With JavaScript
off you get the finished state without the movement.

- **Figures count up** the first time they scroll into view. The script splits
  `£140k` into `£`, `140`, `k` so only the number moves, then writes the
  authored text back at the end. A `setTimeout` backstop does the same if the
  frames dry up, which happens in a background tab: a figure stuck at `£139k`
  would be a quietly wrong number on a page whose whole job is the numbers.
- **Pillar icons draw themselves in.** Each shape is measured with
  `getTotalLength()`, dashed by that length and offset by it, which hides the
  stroke; releasing the offset draws it back on. The solid dot in the second
  icon has no stroke to draw, so it fades in instead.
- **Logos fill with colour on hover.** Neither photo of Marcus has any
  treatment on it: both render as shot, hovered or not.

## The sticky header

Its height is deliberately constant. It sits in normal flow, so shrinking it on
scroll would shorten the document and shunt everything below it upwards, which
also lands anchor jumps underneath the bar. The only thing that changes on
scroll is the hairline along the bottom, via an `is-stuck` class.

It stays cream over the near-black Selected work panel and the green Contact
block rather than inverting per section, which keeps it one predictable object.

Two custom properties, not one:

- `--header-h` drives the header's own `min-height`
- `--header-clear` is what `scroll-margin-top` on the anchor targets uses

They're separate for two reasons. The header ends up taller than its clamp when
the nav wraps to a second line on a narrow screen, so the script measures the
real height into `--header-clear`; predicting that wrap in CSS alone is
guesswork. And feeding a measured height back into `min-height` would pin the
header at its largest size and stop it shrinking again when the window widens.
Without JavaScript, `--header-clear` falls back to `--header-h` and anchor
landings are merely a little tight on narrow screens.

The progress bar along the bottom edge is scaled with `transform: scaleX()`
rather than resized, so dragging the scrollbar doesn't cost a layout on every
frame. It runs even under reduced motion: it tracks the scrollbar rather than
animating on its own, so it's an indicator, not movement.

## Search and sharing

`robots.txt` allows everything, including the AI crawlers that increasingly
answer "who is Marcus Fogg" questions, and points at `sitemap.xml`.

`index.html` carries a JSON-LD `Person` block: job title, employer, location,
what he works on, and the LinkedIn profile as `sameAs`. That's what Google and
the AI crawlers read to build an answer from his own words rather than a
scrape. Keep it in step with the copy when the copy changes.

`assets/img/og-marcus-fogg.jpg` is what LinkedIn and Slack show when the site
is shared. It's rendered from `scripts/og-card.html` by `scripts/og-image.py`,
which pulls the real stylesheet, so it uses the site's own fonts and tokens.
Rerun it after changing the card or the portrait:

```bash
python3 -m http.server 8000 &
python3 scripts/og-image.py
```

`scripts/check.py` renders the live page and shoots the states that are hard to
judge from source: the hover plaques, the logo colours, the photo. It also
reports whether every figure landed on its authored value and whether the icon
strokes were released. Worth running after any change to the motion.

One trap it has already caught: Chromium recomputes `:hover` when the page
scrolls, so a pointer left mid-screen silently hovers whatever scrolls under
it, and "resting" screenshots come out in their hover state. The script parks
the pointer in the corner before every resting shot.

## Replacing the portrait

Drop a new square image in and regenerate the three sizes:

```bash
python3 -c "
from PIL import Image
src = Image.open('new-portrait.jpg').convert('RGB')
for w in (512, 768, 1024):
    im = src.resize((w, w), Image.LANCZOS)
    im.save(f'assets/img/marcus-fogg-{w}.jpg', quality=84, optimize=True, progressive=True)
    im.save(f'assets/img/marcus-fogg-{w}.webp', quality=82, method=6)
"
```

## Notes

- Fonts are self-hosted rather than loaded from Google, so the site makes no
  third-party requests. That's faster, and it sidesteps the GDPR question about
  sending visitor IPs to Google.
- The Work section has two tiers. Crown and Startle are full cards with three
  figures and a link to the live Rocket SaaS case study. Homeflow, StoreFeeder
  and Ami are compact cards with one figure and no link, because those case
  studies aren't published yet. When they go live, move a card up a tier by
  copying the markup of a full card and adding the link.
- **Client sign-off**: the compact cards and the logo strip name clients and
  quote figures from case studies that are still in internal draft. Worth
  squaring off with the clients, and with Rocket, before this goes public.
- Total page weight is roughly 200KB including fonts and the portrait.
