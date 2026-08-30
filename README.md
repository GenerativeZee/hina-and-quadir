# Nikkah Invitation — interactive digital invite

A phone-first invitation website: a sealed embossed envelope that unfolds on tap,
an arched Nikkah hero, a scratch-to-reveal date, the two families, a scrolling
timeline, the venue and a closing note — with background music.

Everything is self-contained. No build step, no CDN, no internet connection
needed. Fonts, artwork and music all ship inside the folder.

---

## Running it

Double-click `index.html` and it works.

For the most reliable result (and to match how it behaves once hosted), serve
the folder instead:

```bash
cd nikkah-invite
python3 -m http.server 8000
# then open http://localhost:8000
```

To put it online, upload the whole folder to any static host — Netlify, Vercel,
GitHub Pages, Hostinger, cPanel, S3. There is no server side.

---

## Personalising it

**Open `details.js`. That is the only file you need to touch.**

Every name, date, time, address and line of copy lives there, commented and in
the order it appears on the page:

| What | Where in `details.js` |
|---|---|
| Wax seal initials | `monogram` |
| Couple's names, ceremony title | `welcome`, `ceremony`, `couple` |
| The date behind the scratch cards | `date.day`, `date.month`, `date.year`, `date.weekday` |
| Both sets of parents | `groom`, `bride` |
| Note to guests | `letterTitle`, `letterBody` |
| Order of the evening | `timeline` — add or remove entries freely |
| Venue and map link | `venue` |
| Closing lines | `closing` |
| Browser tab title | `pageTitle` |

Two things to watch:

- Write an ampersand as `&amp;` — e.g. `couple: "Daanish &amp; Adeena"`.
- `timeline` is a list; add as many `{ time, title, note }` entries as you need
  and the page rebuilds itself around them.

### Changing the music

Drop any `.mp3` into `assets/` and point `music` at it:

```js
music: "assets/their-track.mp3",
musicOnByDefault: true      // false = starts silent, guest taps the note button
```

The shipped `assets/music.mp3` is an original ambient harp loop generated for
this project — no licensing to clear. Music starts on the tap that opens the
envelope, which is what browsers require; the button bottom-right toggles it.

---

## What's in the folder

```
index.html          markup
details.js          ← all client content lives here
css/style.css       styles and all the motion
js/fx.js            atmosphere: gold dust, bokeh, the light burst
js/app.js           the opening, scratch cards, scroll choreography, music
assets/             artwork, fonts, music
tools/              the scripts that generated the artwork and the music
```

Every graphic is hand-built SVG — the embossed floral stock, the wax seal, the
Mughal arch, the lanterns, the gold flourishes and the golden-hour scene. They
are vectors, so they stay sharp on any screen and the whole page is light.

Regenerating artwork is optional and needs only Python:

```bash
python3 tools/make_art.py      # redraws the SVGs into assets/
python3 tools/make_music.py    # rebuilds assets/music.mp3 (needs numpy + ffmpeg)
```

### Changing the colours

The palette is a handful of CSS variables at the top of `css/style.css`:

```css
--ivory   page background
--ink     body text
--gold    headings, rules, ornaments
--script  the calligraphy face
```

For the emboss and gold artwork itself, the colours sit in `tools/make_art.py`
(`emboss()` and `gold()`), then re-run the script.

---

## The opening

Tapping the seal runs a scripted sequence rather than a single transition:

| Time | What happens |
|---|---|
| 0.0s | The wax cracks down a jagged seam, the two halves tumble apart, and a burst of light and gold sparks fires from the centre |
| 0.1s | The top flap swings back; the fold catches the light as it turns |
| 0.5–0.7s | Left, right and bottom flaps unfold in sequence |
| 1.0s | Warm light pools out from inside the envelope |
| 1.4s | The card is uncovered — gold frame, floral corners — and a specular sheen sweeps across it as the monogram lights up |
| 2.8s | The camera pushes in toward the card, blurring as the light swells |
| 3.5s | It passes through into the hero, which rises out of soft focus: the arch draws itself, the lanterns fade in, and the names lift in sequence |

To retime it, change `t1`, `t2` and `t3` near the top of the `envelope()`
function in `js/app.js` — they are the push-in, the pass-through, and the
settle. The individual flap and light timings are the transition delays in the
`ENVELOPE` block of `css/style.css`.

Throughout the page, gold headings catch a sweep of light as they scroll into
view (`.gold-text`), sections fade up with a slight blur and stagger rather
than sliding, the timeline draws its rail and pops each marker, and a fine
layer of gold dust drifts over everything (`js/fx.js`).

Everything above is disabled automatically for anyone who has "reduce motion"
switched on — they get the same invitation, static.

---

## Notes

- Designed phone-first; on desktop it centres as a phone-width card.
- A short preloader holds the first frame until the artwork and fonts are in,
  so the opening never plays half-dressed.
- Works without JavaScript animation for anyone with "reduce motion" turned on.
- If a guest doesn't realise the date cards can be scratched, a "Reveal all"
  link appears after nine seconds.
- Tested on small phones (360px) through desktop.
