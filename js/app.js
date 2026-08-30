/* ═══════════════════════════════════════════════════════════════
   Nikkah invitation — behaviour
   All copy comes from details.js; nothing below needs editing.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var D = window.INVITE || {};
  var $  = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function dig(path) {
    return path.split('.').reduce(function (o, k) {
      return (o == null ? undefined : o[k]);
    }, D);
  }

  /* ── 1. pour the content in ─────────────────────────────────── */
  function fill() {
    if (D.pageTitle) document.title = D.pageTitle;

    $$('[data-fill]').forEach(function (el) {
      var v = dig(el.getAttribute('data-fill'));
      if (v != null) el.innerHTML = v;
    });

    var vals = { day: D.date.day, month: D.date.month, year: D.date.year };
    $$('.card').forEach(function (c) {
      var el = $('.card__value', c), txt = vals[c.getAttribute('data-key')] || '';
      el.innerHTML = txt;
      // long month names need to step down a size or two to fit the card
      if (txt.length > 8) el.classList.add('card__value--xlong');
      else if (txt.length > 5) el.classList.add('card__value--long');
    });
    $('.date__weekday').innerHTML = D.date.weekday || '';

    var ol = $('#tl');
    (D.timeline || []).forEach(function (t, i) {
      var li = document.createElement('li');
      li.className = 'tl__item reveal ' + (i % 2 ? 'reveal--right' : 'reveal--left');
      li.innerHTML =
        '<span class="tl__node"></span>' +
        '<p class="tl__time gold-text">' + t.time + '</p>' +
        '<p class="tl__title">' + t.title + '</p>' +
        (t.note ? '<p class="tl__note">' + t.note + '</p>' : '');
      ol.appendChild(li);
    });
    var end = document.createElement('img');
    end.className = 'tl__end';
    end.src = 'assets/arch-ornament.svg';
    end.alt = '';
    ol.appendChild(end);

    var mb = $('#mapsBtn');
    if (D.venue && D.venue.mapsUrl) mb.href = D.venue.mapsUrl;
    else mb.hidden = true;

    var hb = $('#haldiMapsBtn');
    if (hb) {
      if (D.haldi && D.haldi.mapsUrl) hb.href = D.haldi.mapsUrl;
      else hb.hidden = true;
    }

    var rl = $('#rsvpList');
    if (rl && D.rsvp && D.rsvp.names) {
      D.rsvp.names.forEach(function (nm, i) {
        var li = document.createElement('li');
        li.className = 'rsvp__name';
        li.style.setProperty('--i', i);
        li.innerHTML = nm;
        rl.appendChild(li);
      });
    }

    $('#closingDate').innerHTML =
      [D.date.day, D.date.month, D.date.year].filter(Boolean).join(' &middot; ');

    if (D.music) $('#audio').src = D.music;

    // stagger indices for any group marked data-stagger
    $$('[data-stagger]').forEach(function (g) {
      $$(':scope > *', g).forEach(function (kid, i) {
        kid.style.setProperty('--i', i);
      });
    });
  }

  /* ── 2. the Mughal arch that frames the hero ────────────────── */
  function archPoints(cx, baseY, w, h, n) {
    var half = w / 2,
        d = Math.max((h * h - half * half) / w, 0.001),
        R = half + d,
        cxx = cx + d,
        a0 = Math.PI,
        a1 = Math.atan2(-h, -d);
    while (a1 <= a0) a1 += Math.PI * 2;
    var pts = [], i;
    for (i = 0; i <= n; i++) {
      var a = a0 + (a1 - a0) * (i / n);
      pts.push([cxx + Math.cos(a) * R, baseY + Math.sin(a) * R]);
    }
    for (i = pts.length - 2; i >= 0; i--) pts.push([2 * cx - pts[i][0], pts[i][1]]);
    return pts;
  }

  function plainArch(cx, baseY, w, h, foot) {
    var p = archPoints(cx, baseY, w, h, 48);
    var d = 'M' + p[0][0].toFixed(1) + ',' + foot;
    p.forEach(function (q) { d += 'L' + q[0].toFixed(1) + ',' + q[1].toFixed(1); });
    d += 'L' + p[p.length - 1][0].toFixed(1) + ',' + foot;
    return d;
  }

  function cuspedArch(cx, baseY, w, h, cusps, foot) {
    var p = archPoints(cx, baseY, w, h, cusps);
    var d = 'M' + p[0][0].toFixed(1) + ',' + foot + 'L' + p[0][0].toFixed(1) + ',' + p[0][1].toFixed(1);
    for (var i = 1; i < p.length; i++) {
      var ch = Math.hypot(p[i][0] - p[i - 1][0], p[i][1] - p[i - 1][1]);
      var r = (ch / 2 + 0.01).toFixed(1);
      d += 'A' + r + ',' + r + ' 0 0 1 ' + p[i][0].toFixed(1) + ',' + p[i][1].toFixed(1);
    }
    d += 'L' + p[p.length - 1][0].toFixed(1) + ',' + foot;
    return d;
  }

  var archDrawn = false;

  function drawArch(animate) {
    var svg = $('.hero__arch');
    if (!svg) return;
    var r = svg.getBoundingClientRect();
    var W = Math.round(r.width), H = Math.round(r.height);
    if (!W || !H) return;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);

    var springline = H * 0.44,
        apex = H * 0.05,
        h = springline - apex;
    if (h < W * 0.52) h = W * 0.52;

    var a = $('#archPath'), b = $('#archPath2');
    a.setAttribute('d', plainArch(W / 2, springline, W - 2, h, H));
    b.setAttribute('d', cuspedArch(W / 2, springline + 16, W - 30, h - 6, 15, H));

    [a, b].forEach(function (p) {
      var len = p.getTotalLength();
      p.style.strokeDasharray = len;
      if (animate && !archDrawn && !reduced) {
        p.style.transition = 'none';
        p.style.strokeDashoffset = len;
        void p.getBoundingClientRect();          // flush, so the transition runs
        p.style.transition = '';
        p.style.strokeDashoffset = 0;
      } else {
        p.style.strokeDashoffset = 0;
      }
    });
    if (animate) archDrawn = true;
  }

  /* ── 3. preloader ───────────────────────────────────────────── */
  function boot(done) {
    var art = [
      'assets/envelope-emboss.svg', 'assets/seal.svg', 'assets/hero-scene.svg',
      'assets/corner-spray.svg', 'assets/corner-spray-flip.svg',
      'assets/crest.svg', 'assets/divider.svg',
      'assets/arch-ornament.svg', 'assets/lantern.svg'
    ];
    var bar = $('#bootBar'), loaded = 0, total = art.length + 1, started = Date.now();

    function tick() {
      loaded++;
      if (bar) bar.style.width = Math.round((loaded / total) * 100) + '%';
      if (loaded >= total) finish();
    }

    art.forEach(function (src) {
      var im = new Image();
      im.onload = im.onerror = tick;
      im.src = src;
    });

    if (document.fonts && document.fonts.ready) document.fonts.ready.then(tick);
    else tick();

    var finished = false;
    function finish() {
      if (finished) return;
      finished = true;
      var wait = Math.max(0, 1150 - (Date.now() - started));   // never flash past
      setTimeout(function () {
        $('#boot').classList.add('done');
        done();
      }, wait);
    }
    setTimeout(finish, 6000);                                   // hard ceiling
  }

  /* ── 4. the opening ─────────────────────────────────────────── */
  function envelope() {
    var env    = $('#env'),
        seal   = $('#seal'),
        invite = $('#invite'),
        hero   = $('#hero'),
        opened = false;

    document.body.classList.add('locked');

    function open() {
      if (opened) return;
      opened = true;
      env.classList.add('is-open');
      startMusic();                        // inside the tap, so autoplay is allowed

      // ask for motion access here, while we still have the user's tap
      try {
        var DOE = window.DeviceOrientationEvent;
        if (DOE && typeof DOE.requestPermission === 'function') DOE.requestPermission()['catch'](function () {});
      } catch (e) {}

      // light bursting out of the wax as it cracks — a first, gentle flare
      var r = seal.getBoundingClientRect();
      setTimeout(function () {
        window.FX.burst(r.left + r.width / 2, r.top + r.height / 2, 40);
      }, 90);
      // then a fuller shower as the flaps begin to fall
      setTimeout(function () {
        window.FX.burst(r.left + r.width / 2, r.top + r.height / 2, 72);
      }, reduced ? 140 : 1150);

      var t1 = reduced ? 60  : 4300,       // camera begins to push in
          t2 = reduced ? 160 : 5900,       // through the card, into the hero
          t3 = reduced ? 200 : 7900;       // settle

      // the monogram on the card catches the light once it is uncovered
      setTimeout(function () {
        var m = $('.env__card-mono'); if (m) m.classList.add('lit');
      }, reduced ? 0 : 2300);

      setTimeout(function () { env.classList.add('is-through'); }, t1);

      setTimeout(function () {
        invite.classList.add('is-live');
        invite.setAttribute('aria-hidden', 'false');
        env.classList.add('is-gone');
        document.body.classList.remove('locked');
        window.scrollTo(0, 0);
        drawArch(true);
        hero.classList.add('lit');
        $$('.hero .gold-text').forEach(function (el, i) {
          setTimeout(function () { el.classList.add('lit'); }, 800 + i * 180);
        });
        $('#music').hidden = false;
        requestAnimationFrame(function () { $('#music').classList.add('is-live'); });
      }, t2);

      setTimeout(function () { invite.classList.add('settled'); }, t3);
    }

    seal.addEventListener('click', open);
    env.addEventListener('click', function (e) { if (!seal.contains(e.target)) open(); });

    // deep-link straight past the envelope, e.g. for sharing a section
    var h = (location.hash || '').replace('#', '');
    if (h === 'open' || h === 'invite' || (h && document.getElementById(h))) {
      setTimeout(open, 150);
      var target = document.getElementById(h);
      if (target) setTimeout(function () {
        target.scrollIntoView({ block: 'start' });
      }, reduced ? 300 : 6400);
    }
  }

  /* ── 5. scratch-to-reveal date cards ────────────────────────── */
  function scratch() {
    var cards = $$('.card'), done = 0, hintTimer;

    cards.forEach(function (card) { setupCard(card, finished); });

    function finished() {
      done++;
      if (done === cards.length) {
        clearTimeout(hintTimer);
        $('#revealAll').hidden = true;
        $('#scratchLabel').classList.add('spent');
        setTimeout(function () {
          $('#dateDone').classList.add('in');
          $('.date__weekday').classList.add('lit');
        }, 350);
      }
    }

    hintTimer = setTimeout(function () { $('#revealAll').hidden = false; }, 9000);
    $('#revealAll').addEventListener('click', function () {
      cards.forEach(function (c) { if (!c.classList.contains('done')) c._reveal(); });
    });

    function setupCard(card, onDone) {
      var face = $('.card__face', card),
          cv   = $('.card__foil', card),
          ctx  = cv.getContext('2d'),
          dpr  = Math.min(window.devicePixelRatio || 1, 2),
          w = 0, h = 0, drawing = false, moves = 0, finishedOnce = false;

      function paintFoil() {
        var r = face.getBoundingClientRect();
        w = Math.round(r.width); h = Math.round(r.height);
        if (!w || !h) return;
        cv.style.height = h + 'px';
        cv.width  = Math.round(w * dpr);
        cv.height = Math.round(h * dpr);
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

        var g = ctx.createLinearGradient(0, 0, w, h);
        g.addColorStop(0,   '#F2E3C2');
        g.addColorStop(.28, '#E3CEA2');
        g.addColorStop(.46, '#FAF1DC');
        g.addColorStop(.64, '#DEC59B');
        g.addColorStop(1,   '#EBD9B6');
        ctx.globalCompositeOperation = 'source-over';
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, w, h);

        ctx.strokeStyle = 'rgba(255,248,225,.28)';
        ctx.lineWidth = 1;
        for (var i = -h; i < w; i += 5) {
          ctx.beginPath();
          ctx.moveTo(i, h);
          ctx.lineTo(i + h * .55, 0);
          ctx.globalAlpha = .25 + (i % 17) / 60;
          ctx.stroke();
        }
        ctx.globalAlpha = 1;

        ctx.fillStyle = 'rgba(150,114,60,.30)';
        ctx.font = '400 ' + Math.round(h * .16) + 'px Marcellus, serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('✦', w / 2, h / 2);
        ctx.globalCompositeOperation = 'destination-out';
      }

      function pos(e) {
        var r = cv.getBoundingClientRect();
        return [e.clientX - r.left, e.clientY - r.top];
      }

      function erase(x, y) {
        var rad = Math.min(w, h) * .19;
        ctx.beginPath();
        ctx.arc(x, y, rad, 0, Math.PI * 2);
        ctx.fill();
      }

      function cleared() {
        var d = ctx.getImageData(0, 0, cv.width, cv.height).data,
            gone = 0, total = 0;
        for (var i = 3; i < d.length; i += 4 * 24) { total++; if (d[i] < 40) gone++; }
        return total ? gone / total : 0;
      }

      card._reveal = function () {
        if (finishedOnce) return;
        finishedOnce = true;
        card.classList.add('done');
        var r = cv.getBoundingClientRect();
        window.FX.burst(r.left + r.width / 2, r.top + r.height / 2, 16);
        $('.card__value', card).classList.add('lit');
        onDone();
      };

      cv.addEventListener('pointerdown', function (e) {
        if (finishedOnce) return;
        drawing = true;
        cv.setPointerCapture(e.pointerId);
        var p = pos(e); erase(p[0], p[1]);
        e.preventDefault();
      });
      cv.addEventListener('pointermove', function (e) {
        if (!drawing || finishedOnce) return;
        var p = pos(e); erase(p[0], p[1]);
        if (++moves % 4 === 0) window.FX.spark(e.clientX, e.clientY);
        if (moves % 9 === 0 && cleared() > .5) card._reveal();
        e.preventDefault();
      });
      ['pointerup', 'pointercancel', 'pointerleave'].forEach(function (ev) {
        cv.addEventListener(ev, function () {
          if (!drawing) return;
          drawing = false;
          if (!finishedOnce && cleared() > .38) card._reveal();
        });
      });

      paintFoil();
      window.addEventListener('resize', function () {
        if (!finishedOnce) paintFoil();
        else cv.style.height = face.getBoundingClientRect().height + 'px';
      });
    }
  }

  /* ── 6. scroll choreography + parallax ──────────────────────── */
  function motion() {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        el.classList.add('in');
        // gold headings catch the light as they arrive
        if (el.classList.contains('gold-text')) el.classList.add('lit');
        $$('.gold-text', el).forEach(function (g, i) {
          setTimeout(function () { g.classList.add('lit'); }, 140 + i * 120);
        });
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: .12 });

    $$('.reveal').forEach(function (el) { io.observe(el); });
    var rail = $('#tlRail');
    if (rail) io.observe(rail);

    if (reduced) return;

    /* the date cards tip in 3D toward a fine pointer */
    if (window.matchMedia('(pointer:fine)').matches) {
      var cardWrap = $('#cards');
      if (cardWrap) {
        $$('.card', cardWrap).forEach(function (card) {
          card.addEventListener('pointermove', function (e) {
            var r = card.getBoundingClientRect();
            var gx = (e.clientX - r.left) / r.width - .5;
            var gy = (e.clientY - r.top) / r.height - .5;
            card.style.transform =
              'rotateX(' + (-gy * 14).toFixed(2) + 'deg) rotateY(' +
              (gx * 16).toFixed(2) + 'deg) translateZ(14px)';
          });
          card.addEventListener('pointerleave', function () {
            card.style.transform = '';
          });
        });
      }
    }

    /* hero: a small room seen through the frame — every plane sits at its
       own depth, and the whole room banks toward the pointer / phone tilt */
    var hero  = $('#hero'),
        depth = $('#heroDepth'),
        pScene   = $('.hero__plane--scene'),
        pArch    = $('.hero__plane--arch'),
        pCorners = $('.hero__plane--corners'),
        pLant    = $('.hero__plane--lanterns'),
        pGarland = $('.hero__plane--garland');

    // tx/ty = where we want to be (-1..1); cx/cy = eased current
    var tx = 0, ty = 0, cx = 0, cy = 0, sc = 0, running = false, idle = 0;

    function apply() {
      // far things move against the pointer, near things with it
      depth.style.transform =
        'rotateX(' + (cy * -4.5).toFixed(2) + 'deg) rotateY(' + (cx * 6).toFixed(2) + 'deg)';
      if (pScene) pScene.style.transform =
        'translate3d(' + (cx * -14).toFixed(1) + 'px,' + (sc * .22 + cy * -11).toFixed(1) + 'px,0) translateZ(-170px) scale(1.28)';
      if (pArch) pArch.style.transform =
        'translate3d(' + (cx * -7).toFixed(1) + 'px,' + (sc * .10 + cy * -6).toFixed(1) + 'px,0) translateZ(-55px)';
      if (pCorners) pCorners.style.transform =
        'translate3d(' + (cx * 13).toFixed(1) + 'px,' + (sc * .05 + cy * 9).toFixed(1) + 'px,0) translateZ(24px)';
      if (pLant) pLant.style.transform =
        'translate3d(' + (cx * 22).toFixed(1) + 'px,' + (sc * -.02 + cy * 15).toFixed(1) + 'px,0) translateZ(70px)';
      if (pGarland) pGarland.style.transform =
        'translate3d(' + (cx * 30).toFixed(1) + 'px,' + (sc * -.06 + cy * 21).toFixed(1) + 'px,0) translateZ(105px)';
    }

    function loop() {
      running = true;
      var y = window.scrollY || 0;
      sc = (y > hero.offsetHeight + 200) ? sc : y;
      cx += (tx - cx) * .08;
      cy += (ty - cy) * .08;
      apply();
      var moving = Math.abs(tx - cx) + Math.abs(ty - cy) > .001;
      if (moving) { idle = 0; }
      else if (++idle > 30) { running = false; return; }
      requestAnimationFrame(loop);
    }
    function kick() { if (!running) requestAnimationFrame(loop); }

    window.addEventListener('scroll', kick, { passive: true });
    apply();

    if (window.matchMedia('(pointer:fine)').matches) {
      hero.addEventListener('pointermove', function (e) {
        var r = hero.getBoundingClientRect();
        tx = ((e.clientX - r.left) / r.width - .5) * 2;
        ty = ((e.clientY - r.top) / r.height - .5) * 2;
        kick();
      });
      hero.addEventListener('pointerleave', function () { tx = ty = 0; kick(); });
    }

    // phone tilt — uses the real depth of the screen
    window.addEventListener('deviceorientation', function (e) {
      if (e.gamma == null && e.beta == null) return;
      var g = Math.max(-1, Math.min(1, (e.gamma || 0) / 26));
      var b = Math.max(-1, Math.min(1, ((e.beta || 0) - 42) / 26));
      tx = g; ty = b; kick();
    }, true);
  }

  /* ── 7. music ───────────────────────────────────────────────── */
  var audio, btn;
  function startMusic() {
    if (!D.musicOnByDefault || !D.music) return;
    audio.volume = 0;
    var p = audio.play();
    if (p && p.catch) p.catch(function () { btn.classList.remove('playing'); });
    btn.classList.add('playing');
    var v = 0, fade = setInterval(function () {
      v = Math.min(v + .03, .55);
      audio.volume = v;
      if (v >= .55) clearInterval(fade);
    }, 110);
  }

  function music() {
    audio = $('#audio');
    btn = $('#music');
    btn.addEventListener('click', function () {
      if (audio.paused) {
        audio.volume = .55;
        audio.play();
        btn.classList.add('playing');
      } else {
        audio.pause();
        btn.classList.remove('playing');
      }
    });
    audio.addEventListener('error', function () { btn.hidden = true; });
  }

  /* ── capture / preview mode (?cap) — for screenshots only ───── */
  if (/[?&]cap\b/.test(location.search)) {
    var st = document.createElement('style');
    st.textContent =
      '#boot{display:none!important}' +
      '.env{display:none!important}' +
      '.invite{opacity:1!important;transform:none!important;filter:none!important}' +
      '.hero{height:100svh!important;perspective:none!important}' +
      '.hero__depth,.hero__plane{transform:none!important;transform-style:flat!important}' +
      '.hero__scene{animation:none!important;transform:none!important;opacity:1!important}' +
      '.hero__archimg,.hero__lantern,.hero__flora,.hero__bloom,.hero__haze{opacity:1!important;transform:none!important}' +
      '.hero__flora--tr{transform:scaleX(-1)!important}.hero__flora--bl{transform:scaleY(-1)!important}.hero__flora--br{transform:scale(-1)!important}' +
      '.reveal,.hl{opacity:1!important;transform:none!important;filter:none!important}' +
      '.date__done,.date__done .date__laurel{opacity:1!important;transform:translate(-50%,-52%) scale(1)!important}' +
      '.date__done{transform:none!important}' +
      '.tl__rail{transform:translateX(-.5px) scaleY(1)!important}' +
      '.tl__node{transform:rotate(45deg) scale(1)!important}';
    document.head.appendChild(st);
    document.documentElement.classList.add('cap');
    var hp = document.getElementById('hero'); if (hp) hp.classList.add('lit');
  }

  /* ── go ─────────────────────────────────────────────────────── */
  fill();
  window.FX.init();
  music();
  envelope();
  scratch();
  motion();
  drawArch(false);
  window.addEventListener('resize', function () { drawArch(false); });
  window.addEventListener('orientationchange', function () { setTimeout(function () { drawArch(false); }, 260); });

  boot(function () {
    $('#env').classList.add('is-here');
  });
})();
