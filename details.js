/* ═══════════════════════════════════════════════════════════════════
   EDIT EVERYTHING HERE.
   This is the only file you need to touch to personalise the invite.
   Nothing else in the project contains client details.
   ═══════════════════════════════════════════════════════════════════ */

window.INVITE = {

  /* ── Browser tab ───────────────────────────────────────────────── */
  pageTitle: "Daanish & Adeena — Nikkah Invitation",

  /* ── The sealed envelope ───────────────────────────────────────── */
  monogram: "D&A",                 // the initials pressed into the wax seal
  openHint: "Tap the seal to open",
  cardTeaser: "With the blessings of Allah",

  /* ── Hero ──────────────────────────────────────────────────────── */
  welcome: "Welcome to the",
  ceremony: "Nikkah Ceremony",
  joiner: "of",
  couple: "Daanish &amp; Adeena",   // use &amp; for the ampersand
  scrollCue: "Scroll down",

  /* ── The date (revealed by scratching) ─────────────────────────── */
  date: {
    day: "10",
    month: "January",
    year: "2027",
    weekday: "Sunday",
    scratchLabel: "Scratch to reveal the date",
    revealedNote: "Do save the date"
  },

  /* ── The two families ──────────────────────────────────────────── */
  groom: {
    name: "Daanish",
    relation: "Son of",
    parents: "Mr &amp; Mrs A. Siddiqui"
  },
  bride: {
    name: "Adeena",
    relation: "Daughter of",
    parents: "Mr &amp; Mrs Ch. Farooqi"
  },

  /* ── The note to guests ────────────────────────────────────────── */
  letterTitle: "Dear Friends and Family",
  letterBody:
    "Join us for an evening of love, laughter, duas, and unforgettable " +
    "memories as we begin our forever.",

  /* ── Order of the evening ──────────────────────────────────────── */
  timelineTitle: "Wedding Timeline",
  timeline: [
    { time: "6:00 PM", title: "Guest Arrival",   note: "Welcome drinks" },
    { time: "7:00 PM", title: "Nikkah Ceremony", note: "Followed by duas" },
    { time: "8:00 PM", title: "Dinner",          note: "Served in the courtyard" },
    { time: "9:30 PM", title: "Celebrations",    note: "Music and dancing" },
    { time: "11:00 PM", title: "Rukhsati",       note: "A farewell with love" }
  ],

  /* ── Where ─────────────────────────────────────────────────────── */
  venue: {
    title: "The Venue",
    name: "Falaknuma Banquet Hall",
    address: "12 Rose Garden Road, Banjara Hills, Hyderabad 500034",
    mapsUrl: "https://maps.google.com/?q=Banjara+Hills+Hyderabad",
    mapsLabel: "Open in Maps"
  },

  /* ── Closing ───────────────────────────────────────────────────── */
  closing: {
    line1: "We cannot wait to celebrate",
    line2: "with you",
    signoff: "Daanish &amp; Adeena"
  },

  /* ── Music ─────────────────────────────────────────────────────── */
  // Drop any .mp3 into assets/ and point this at it to change the track.
  music: "assets/music.mp3",
  musicOnByDefault: true
};
