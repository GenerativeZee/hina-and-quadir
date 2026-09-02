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
  // the Bismillah calligraphy on the card is an image — see assets/bismillah.png

  /* ── Hero ──────────────────────────────────────────────────────── */
  welcome: "إِنْ شَاءَ اللّٰه",       // "In Sha Allah" in Arabic
  ceremony: "Nikah Ceremony",
  joiner: "of",
  couple: "Hina&nbsp;&amp;<br>Quadir",   // &amp; = ampersand; <br> keeps it two tidy lines
  scrollCue: "Scroll to begin",

  /* ── The date (revealed by scratching) ─────────────────────────── */
  date: {
    day: "14",
    month: "November",
    year: "2026",
    hijri: "4 Jumada al-Thani &middot; 1448 AH",
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

  /* ── A verse of the Qur'an, in place of the note to guests ─────── */
  ayah: {
    arabic:
      "وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ<br>" +
      "أَزْوَاجًا لِّتَسْكُنُوا إِلَيْهَا",
    translation:
      "&ldquo;And of His signs is that He created for you from " +
      "yourselves mates that you may find tranquility in them.&rdquo;",
    reference: "Al-Qur&rsquo;an &bull; Surah Ar-Rum 30:21"
  },

  /* ── Order of the celebrations ─────────────────────────────────── */
  timelineTitle: "The Celebrations",
  timeline: [
    { time: "14 Nov", title: "Nikah Ceremony", note: "Saturday &middot; 7:00 PM onwards" },
    { time: "Thereafter", title: "Dinner", note: "Served following the Nikah" }
  ],

  /* ── Where (the Nikah) ─────────────────────────────────────────── */
  venue: {
    title: "The Venue",
    name: "Habib Garden",
    address: "Marris Road, Aligarh, Uttar Pradesh",
    mapsUrl: "https://maps.google.com/?q=Habib+Garden+Marris+Road+Aligarh",
    mapsLabel: "Open in Maps"
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

  /* ── With warm regards — compliments & contact ─────────────────── */
  regards: {
    eyebrow: "With Warm Regards",
    title: "Compliments &amp;<br>Contact",
    fromLabel: "With Best Compliments From",
    guardian: "Mrs. Nasreen Rafiq, W/o Late Mohd. Rafiq",
    phone: "9760252105",
    reachLabel: "For R.S.V.P. &amp; enquiries, please reach out to",
    rsvpName: "Mohd Amir Rafiq",
    rsvpSub: "&amp; all brothers and relatives"
  },

  /* ── Music ─────────────────────────────────────────────────────── */
  // Drop any .mp3 into assets/ and point this at it to change the track.
  music: "assets/music.mp3",
  musicOnByDefault: true
};
