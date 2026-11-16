/* SQL Quest · shared pixel-study script · datawithkim.dev
 * Any page that loads this file gets:
 *  - the walking cat on the reading bar (.track)
 *  - a cat in every save point (.save)
 *  - the sleeping-cat scene (.scene-slot)
 *  - hover definitions for .term buttons + an auto glossary (#gloss)
 *  - "cleared" checkboxes with progress (.clear input[data-ch]) saved per episode
 *  - a quiz from window.QUIZ into #quizbox
 *  - the Pomodoro timer + soft rain dock
 * Episode pages set <body data-ep="ep01"> so the hub page can show progress.
 */
(function () {
  'use strict';

  var SPRITES = {
    sit: '{SPRITE_SIT}',
    walk: '{SPRITE_WALK}',
    scene: '{SCENE}'
  };

  function store(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); }
    catch (e) { return null; }
  }
  function svg(name, cls) { return SPRITES[name].replace('<svg ', '<svg class="' + cls + '" '); }
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }

  var EP = document.body.dataset.ep || null;
  window.SQLQuest = {
    epKey: function (ep) { return 'sqlquest-' + ep + '-cleared'; },
    doneKey: function (ep) { return 'sqlquest-' + ep + '-done'; },
    isDone: function (ep) { return store('sqlquest-' + ep + '-done') === '1'; },
    store: store,
    cat: function (cls) { return svg('sit', cls || 'cat'); }
  };

  document.addEventListener('DOMContentLoaded', function () {
    var yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();

    /* ---------- sprites ---------- */
    $$('.scene-slot').forEach(function (el) { el.innerHTML = svg('scene', 'scene'); });
    $$('.save').forEach(function (el) { el.insertAdjacentHTML('afterbegin', svg('sit', 'cat')); });
    $$('.cat-slot').forEach(function (el) { el.innerHTML = svg('sit', el.dataset.cls || 'cat'); });

    /* ---------- reading track + walking cat ---------- */
    var track = $('.track');
    if (track) {
      track.insertAdjacentHTML('beforeend', '<div class="fill" id="fill"></div>' + svg('walk', 'walker idle'));
      var fill = $('#fill'), walker = $('.walker'), lastP = 0, idleT;
      var onScroll = function () {
        var h = document.documentElement, p = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight);
        p = Math.min(1, Math.max(0, p));
        fill.style.width = (p * 100) + '%';
        walker.style.left = 'calc(' + (p * 100) + '% * 0.96 + 14px)';
        walker.classList.toggle('flip', p < lastP);
        walker.classList.remove('idle'); clearTimeout(idleT);
        idleT = setTimeout(function () { walker.classList.add('idle'); }, 250);
        lastP = p;
      };
      window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
    }

    /* ---------- reveal on scroll ---------- */
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { threshold: 0.08 });
      $$('.reveal').forEach(function (el) { io.observe(el); });
    } else { $$('.reveal').forEach(function (el) { el.classList.add('in'); }); }

    /* ---------- cleared chapters / levels ---------- */
    var boxes = $$('.clear input[data-ch]');
    if (EP && boxes.length) {
      var total = boxes.length, cleared = {};
      try { cleared = JSON.parse(store(SQLQuest.epKey(EP)) || '{}') || {}; } catch (e) { cleared = {}; }
      var paint = function () {
        var n = 0;
        boxes.forEach(function (cb) {
          var on = !!cleared[cb.dataset.ch]; if (on) n++;
          cb.checked = on;
          var lvl = $('.lvl[data-ch="' + cb.dataset.ch + '"]'); if (lvl) lvl.classList.toggle('done', on);
        });
        var xp = $('#xp'); if (xp) xp.textContent = (n === total ? total + '/' + total + ' ✓' : n + '/' + total);
        store(SQLQuest.doneKey(EP), n === total ? '1' : '0');
      };
      boxes.forEach(function (cb) {
        cb.addEventListener('change', function () {
          cleared[cb.dataset.ch] = cb.checked; store(SQLQuest.epKey(EP), JSON.stringify(cleared)); paint();
        });
      });
      paint();
    }

    /* ---------- tooltips + glossary ---------- */
    var tip = document.createElement('div'); tip.id = 'tip'; tip.setAttribute('role', 'tooltip');
    document.body.appendChild(tip);
    var showTip = function (el) {
      tip.textContent = el.dataset.def;
      var r = el.getBoundingClientRect();
      tip.classList.add('on');
      var x = Math.min(window.innerWidth - tip.offsetWidth - 10, Math.max(10, r.left));
      var y = r.top - tip.offsetHeight - 10; if (y < 70) y = r.bottom + 10;
      tip.style.left = x + 'px'; tip.style.top = y + 'px';
    };
    var hideTip = function () { tip.classList.remove('on'); };
    var bindTip = function (el) {
      el.addEventListener('mouseenter', function () { showTip(el); });
      el.addEventListener('focus', function () { showTip(el); });
      el.addEventListener('click', function () { showTip(el); });
      el.addEventListener('mouseleave', hideTip);
      el.addEventListener('blur', hideTip);
    };
    var gl = $('#gloss'), seen = {};
    $$('.term').forEach(function (term) {
      bindTip(term);
      if (!gl) return;
      var name = term.textContent; if (seen[name]) return; seen[name] = 1;
      var d = document.createElement('div'); d.className = 'px gcard';
      var dt = document.createElement('dt'); dt.textContent = name;
      var dd = document.createElement('dd'); dd.textContent = term.dataset.def;
      d.appendChild(dt); d.appendChild(dd); gl.appendChild(d);
    });
    $$('.bar-row').forEach(function (r) { r.dataset.def = r.dataset.tip; bindTip(r); });
    window.addEventListener('scroll', hideTip, { passive: true });

    /* ---------- quiz ---------- */
    var box = $('#quizbox');
    if (box && window.QUIZ) {
      var Q = window.QUIZ, score = 0, answered = 0;
      Q.forEach(function (item, i) {
        var q = document.createElement('div'); q.className = 'q';
        var p = document.createElement('p'); p.textContent = (i + 1) + '. ' + item.q; q.appendChild(p);
        var opts = document.createElement('div'); opts.className = 'opts';
        var why = document.createElement('div'); why.className = 'why';
        item.o.forEach(function (txt, j) {
          var b = document.createElement('button'); b.type = 'button'; b.textContent = txt;
          b.addEventListener('click', function () {
            $$('button', opts).forEach(function (x, k) { x.disabled = true; if (k === item.a) x.classList.add('right'); });
            if (j !== item.a) b.classList.add('wrong'); else score++;
            why.textContent = (j === item.a ? '✓ ' : '✗ ') + item.w;
            answered++; if (answered === Q.length) showScore();
          });
          opts.appendChild(b);
        });
        q.appendChild(opts); q.appendChild(why); box.appendChild(q);
      });
      var res = document.createElement('div'); res.className = 'score'; box.appendChild(res);
      var showScore = function () {
        res.innerHTML = svg('sit', 'sc') + '<span></span>';
        $('span', res).textContent = 'score: ' + score + '/' + Q.length +
          (score === Q.length ? ' · purrfect!' : score >= Q.length * 0.6 ? ' · nice, almost there' : ' · reread a level and try again');
      };
    }

    /* ---------- study dock: pomodoro + rain ---------- */
    if (document.body.dataset.dock !== 'off') buildDock();
  });

  function buildDock() {
    var d = document.createElement('aside');
    d.className = 'px dock'; d.id = 'dock'; d.setAttribute('aria-label', 'Study timer');
    d.innerHTML =
      '<div class="row"><span class="lbl">pomodoro</span><span class="mode" id="mode">focus</span>' +
      '<button class="tog" id="tog" aria-label="Minimise timer" title="minimise">_</button></div>' +
      '<div class="body"><div class="row" style="margin-top:2px"><span class="time" id="time" aria-live="polite">25:00</span>' +
      svg('sit', 'mini') + '</div><div class="btns"><button id="start">start</button><button id="reset">reset</button>' +
      '<button id="rain" aria-pressed="false" title="Soft rain sound">rain</button></div></div>';
    document.body.appendChild(d);

    var FOCUS = 25 * 60, BREAK = 5 * 60, left = FOCUS, onBreak = false, timer = null;
    var tEl = document.getElementById('time'), mEl = document.getElementById('mode'), sBtn = document.getElementById('start');
    var baseTitle = document.title;
    var fmt = function (s) { return String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0'); };
    var draw = function () {
      tEl.textContent = fmt(left); mEl.textContent = onBreak ? 'break ☕' : 'focus';
      document.title = (timer ? fmt(left) + ' · ' : '') + baseTitle;
    };
    var chime = function () {
      try {
        var C = window.AudioContext || window.webkitAudioContext, c = new C();
        [660, 880].forEach(function (f, i) {
          var o = c.createOscillator(), g = c.createGain(), t0 = c.currentTime + i * .18;
          o.type = 'square'; o.frequency.value = f;
          g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(0.05, t0 + .02);
          g.gain.exponentialRampToValueAtTime(0.0001, t0 + .16);
          o.connect(g); g.connect(c.destination); o.start(t0); o.stop(t0 + .2);
        });
      } catch (e) {}
    };
    var tick = function () {
      left--;
      if (left <= 0) { chime(); onBreak = !onBreak; left = onBreak ? BREAK : FOCUS; }
      draw();
    };
    sBtn.addEventListener('click', function () {
      if (timer) { clearInterval(timer); timer = null; sBtn.textContent = 'start'; }
      else { timer = setInterval(tick, 1000); sBtn.textContent = 'pause'; }
      draw();
    });
    document.getElementById('reset').addEventListener('click', function () {
      clearInterval(timer); timer = null; onBreak = false; left = FOCUS; sBtn.textContent = 'start'; draw();
    });
    var tog = document.getElementById('tog');
    var setMin = function (m) {
      d.classList.toggle('min', m); tog.textContent = m ? '+' : '_';
      tog.setAttribute('aria-label', m ? 'Expand timer' : 'Minimise timer');
    };
    tog.addEventListener('click', function () { setMin(!d.classList.contains('min')); });
    if (window.innerWidth < 860) setMin(true);
    draw();

    var rainCtx = null, rainGain = null, rBtn = document.getElementById('rain');
    rBtn.addEventListener('click', function () {
      try {
        if (!rainCtx) {
          var C = window.AudioContext || window.webkitAudioContext; rainCtx = new C();
          var len = 2 * rainCtx.sampleRate, buf = rainCtx.createBuffer(1, len, rainCtx.sampleRate), data = buf.getChannelData(0), last = 0;
          for (var i = 0; i < len; i++) { var w = Math.random() * 2 - 1; last = (last + 0.02 * w) / 1.02; data[i] = last * 3.5; }
          var src = rainCtx.createBufferSource(); src.buffer = buf; src.loop = true;
          var lp = rainCtx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 1200;
          rainGain = rainCtx.createGain(); rainGain.gain.value = 0;
          src.connect(lp); lp.connect(rainGain); rainGain.connect(rainCtx.destination); src.start();
        }
        var on = rBtn.getAttribute('aria-pressed') !== 'true';
        rainCtx.resume();
        rainGain.gain.setTargetAtTime(on ? 0.35 : 0, rainCtx.currentTime, 0.4);
        rBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
      } catch (e) { rBtn.disabled = true; rBtn.title = 'Sound not available in this browser'; }
    });
  }
})();
