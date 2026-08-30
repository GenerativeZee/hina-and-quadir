/* ═══════════════════════════════════════════════════════════════════
   EDIT EVERYTHING HERE.
   This is the only file you need to touch to personalise the invite.
   Nothing else in the project contains client details.
   ═══════════════════════════════════════════════════════════════════ */

window.INVITE = {

  /* ── Browser tab ───────────────────────────────────────────────── */
  pageTitle: "Hina & Quadir — Nikah Invitation",

  /* ── The sealed envelope ───────────────────────────────────────── */
  monogram: "H&Q",                 // the initials pressed into the wax seal
  openHint: "Tap the seal to open",
  cardTeaser: "In the name of Allah",

  /* ── Hero ──────────────────────────────────────────────────────── */
  welcome: "In Sha Allah",
  ceremony: "Nikah Ceremony",
  joiner: "of",
  couple: "Hina &amp; Quadir",      // use &amp; for the ampersand
  scrollCue: "Scroll to begin",

  /* ── The date (revealed by scratching) ─────────────────────────── */
  date: {
    day: "14",
    month: "November",
    year: "2026",
    weekday: "Saturday",
    scratchLabel: "Scratch to reveal the date",
    revealedNote: "Do save the date"
  },

  /* ── The two families ──────────────────────────────────────────── */
  groom: {
    name: "Md. Quadir",
    relation: "Son of",
    parents: "Mr Syed Mohd. Manzar Imam"
  },
  bride: {
    name: "Hina Rafiq",
    relation: "Daughter of",
    parents: "Mrs Nasreen Rafiq &middot; Wife of Late Mohd. Rafiq"
  },

  /* ── The note to guests ────────────────────────────────────────── */
  letterTitle: "Bismillah ir-Rahman ir-Rahim",
  letterBody:
    "Mrs. Nasreen Rafiq requests the honour of your presence on the " +
    "auspicious occasion of the Nikah ceremony of her beloved daughter " +
    "Hina, as two families are joined as one by the grace of Allah.",

  /* ── Order of the celebrations ─────────────────────────────────── */
  timelineTitle: "The Celebrations",
  timeline: [
    { time: "12 Nov", title: "Haldi Ceremony", note: "Thursday, 7:00 PM · Zayan Garden, Aligarh" },
    { time: "14 Nov", title: "Nikah Ceremony", note: "Saturday, 7:00 PM onwards · Habib Garden" },
    { time: "Thereafter", title: "Dinner",     note: "Served following the Nikah, In Sha Allah" }
  ],

  /* ── Where (the Nikah) ─────────────────────────────────────────── */
  venue: {
    title: "The Venue",
    name: "Habib Garden",
    address: "Marris Road, Aligarh, Uttar Pradesh",
    mapsUrl: "https://maps.google.com/?q=Habib+Garden+Marris+Road+Aligarh",
    mapsLabel: "Open in Maps"
  },

  /* ── The Haldi ceremony ────────────────────────────────────────── */
  haldi: {
    title: "Haldi Ceremony",
    intro: "We cordially invite you to the Haldi ceremony of",
    name: "Hina Rafiq",
    datetime: "Thursday, 12th November 2026 &middot; 7:00 PM onwards",
    venueName: "Zayan Garden",
    venueAddr: "Manzoor Gandhi Road, Aligarh",
    mapsUrl: "https://maps.google.com/?q=Zayan+Garden+Manzoor+Gandhi+Road+Aligarh",
    mapsLabel: "Open in Maps",
    note: "Your presence will make this occasion even more special"
  },

  /* ── R.S.V.P. ──────────────────────────────────────────────────── */
  rsvp: {
    title: "R.S.V.P.",
    intro: "Kindly confirm your presence with",
    names: [
      "Mohd. Amir Rafiq",
      "Danish Hussain Khan",
      "Diyan Hussain Khan",
      "Ammar Amir"
    ]
  },

  /* ── Closing ───────────────────────────────────────────────────── */
  closing: {
    line1: "Your presence will make this",
    line2: "occasion even more special",
    signoff: "Hina &amp; Quadir"
  },

  /* ── Music ─────────────────────────────────────────────────────── */
  // Drop any .mp3 into assets/ and point this at it to change the track.
  music: "assets/music.mp3",
  musicOnByDefault: true
};
