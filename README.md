# marcusfogg.com

Single-page personal portfolio site. Plain HTML and CSS, no build step and no
framework. Open `index.html` in a browser and it works.

The header links are anchors to sections on the one page: Work, About, Approach,
Contact. The only JavaScript is fifteen lines at the bottom of `index.html` that
underline whichever nav item is in view. Turn JavaScript off and the nav still
works, it just stops highlighting.

## What's in here

```
index.html                     the homepage
assets/css/styles.css          all styling, design tokens at the top
assets/fonts/                  Cormorant + Instrument Sans (self-hosted .woff2)
assets/img/                    portrait at 3 sizes, WebP + JPEG, plus favicon
assets/files/marcus-fogg-cv.pdf  the CV the site links to
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

`assets/img/logos/` holds two sets, both made from the colour originals by
`scripts/logos.py`: every non-white pixel becomes the target colour, and white
becomes transparent.

- `*-white.png` for the five clients, used on the dark Selected Work cards
- `*-ink.png` for the six employers, used on the cream Where I've worked row

It's a knockout rather than a flatten, which is why Crown's crown, Homeflow's
chevron, Famly's heart and Reload's arrow still read as shapes. They're cut out
of the mark rather than drawn on top of it.

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
so they add nothing to page weight, but keeping them means the mono versions
can be regenerated without hunting the files down again.

A logo with a gradient or a photographic element flattens to a white blob. If a
client's brand kit has an official reversed or mono version, use that instead
of converting the colour one.

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
