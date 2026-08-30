/* ═══════════════════════════════════════════════════════════════
   Atmosphere — drifting gold dust, soft bokeh, and the light burst
   that fires when the wax seal breaks.

   One canvas, transform-free, capped particle counts. Sits above the
   page and never takes pointer events.
   ═══════════════════════════════════════════════════════════════ */
window.FX = (function () {
  'use strict';

  var cv, ctx, W = 0, H = 0, dpr = 1,
      motes = [], bokeh = [], sparks = [],
      running = false, raf = 0, t = 0,
      reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function rand(a, b) { return a + Math.random() * (b - a); }

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth;
    H = window.innerHeight;
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(H * dpr);
    cv.style.width = W + 'px';
    cv.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    seed();
  }

  function seed() {
    // density scales with the viewport but stays modest on big screens
    var n = Math.round(Math.min(58, Math.max(24, (W * H) / 14000)));
    motes = [];
    for (var i = 0; i < n; i++) motes.push(newMote(true));

    bokeh = [];
    for (var j = 0; j < 5; j++) {
      bokeh.push({
        x: rand(0, W), y: rand(0, H),
        r: rand(38, 96),
        a: rand(.030, .075),
        vy: rand(-.10, -.03),
        vx: rand(-.05, .05),
        ph: rand(0, 6.28)
      });
    }
  }

  function newMote(anywhere) {
    return {
      x: rand(-20, W + 20),
      y: anywhere ? rand(0, H) : H + rand(10, 90),
      r: rand(.5, 2.1),
      vy: rand(-.30, -.07),
      sway: rand(.15, .55),
      ph: rand(0, 6.28),
      a: rand(.22, .72),
      tw: rand(.6, 1.9)                    // twinkle speed
    };
  }

  function draw() {
    raf = 0;
    if (!running) return;
    t += 1 / 60;
    ctx.clearRect(0, 0, W, H);

    // soft out-of-focus lights
    for (var b = 0; b < bokeh.length; b++) {
      var o = bokeh[b];
      o.x += o.vx; o.y += o.vy;
      if (o.y < -o.r) { o.y = H + o.r; o.x = rand(0, W); }
      if (o.x < -o.r) o.x = W + o.r;
      if (o.x > W + o.r) o.x = -o.r;
      var pulse = o.a * (.75 + .25 * Math.sin(t * .6 + o.ph));
      var g = ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, o.r);
      g.addColorStop(0, 'rgba(255,240,206,' + pulse.toFixed(3) + ')');
      g.addColorStop(1, 'rgba(255,240,206,0)');
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(o.x, o.y, o.r, 0, 6.2832); ctx.fill();
    }

    // drifting dust
    for (var i = 0; i < motes.length; i++) {
      var m = motes[i];
      m.y += m.vy;
      m.x += Math.sin(t * m.sway + m.ph) * .28;
      if (m.y < -12) motes[i] = newMote(false);
      var tw = m.a * (.55 + .45 * Math.sin(t * m.tw + m.ph));
      ctx.fillStyle = 'rgba(255,244,219,' + tw.toFixed(3) + ')';
      ctx.beginPath(); ctx.arc(m.x, m.y, m.r, 0, 6.2832); ctx.fill();
      if (m.r > 1.5) {                       // a faint halo on the larger motes
        ctx.fillStyle = 'rgba(233,199,134,' + (tw * .22).toFixed(3) + ')';
        ctx.beginPath(); ctx.arc(m.x, m.y, m.r * 2.6, 0, 6.2832); ctx.fill();
      }
    }

    // the burst from the breaking seal
    for (var s = sparks.length - 1; s >= 0; s--) {
      var p = sparks[s];
      p.vy += p.g;
      p.vx *= .985; p.vy *= .985;
      p.x += p.vx; p.y += p.vy;
      p.life -= 1;
      if (p.life <= 0) { sparks.splice(s, 1); continue; }
      var k = p.life / p.max;
      ctx.globalAlpha = k * k;
      ctx.fillStyle = p.warm
        ? 'rgba(255,229,168,1)'
        : 'rgba(255,250,238,1)';
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r * (.35 + k * .65), 0, 6.2832); ctx.fill();
      if (p.r > 1.6) {
        ctx.globalAlpha = k * .28;
        ctx.fillStyle = 'rgba(226,183,116,1)';
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r * 3.4 * k, 0, 6.2832); ctx.fill();
      }
      ctx.globalAlpha = 1;
    }

    raf = requestAnimationFrame(draw);
  }

  function start() {
    if (running || reduced) return;
    running = true;
    if (!raf) raf = requestAnimationFrame(draw);
  }
  function stop() {
    running = false;
    if (raf) { cancelAnimationFrame(raf); raf = 0; }
  }

  return {
    init: function () {
      cv = document.getElementById('fx');
      if (!cv) return;
      ctx = cv.getContext('2d');
      resize();
      window.addEventListener('resize', function () {
        clearTimeout(resize._t);
        resize._t = setTimeout(resize, 200);
      });
      document.addEventListener('visibilitychange', function () {
        if (document.hidden) stop(); else start();
      });
      if (reduced) { cv.style.display = 'none'; return; }
      start();
    },

    /* a shower of light from a point — used when the seal cracks */
    burst: function (x, y, n) {
      if (reduced) return;
      n = n || 54;
      for (var i = 0; i < n; i++) {
        var a = rand(0, 6.2832), sp = rand(1.4, 7.2), life = rand(46, 108);
        sparks.push({
          x: x, y: y,
          vx: Math.cos(a) * sp,
          vy: Math.sin(a) * sp - rand(.4, 2.0),
          g: rand(.028, .062),
          r: rand(.8, 2.6),
          life: life, max: life,
          warm: Math.random() < .68
        });
      }
      start();
    },

    /* two or three glints — used while a card is being scratched */
    spark: function (x, y) {
      if (reduced || sparks.length > 160) return;
      for (var i = 0; i < 3; i++) {
        var a = rand(0, 6.2832), sp = rand(.5, 2.2), life = rand(20, 44);
        sparks.push({
          x: x, y: y,
          vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - .5,
          g: .05, r: rand(.6, 1.5),
          life: life, max: life, warm: true
        });
      }
      start();
    },

    reduced: reduced
  };
})();
