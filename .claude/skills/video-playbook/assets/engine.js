(function () {
  var GLOSS = __GLOSS__;
  var YT = "__VIDEO_URL__";
  function secs(s) { var p = s.split(":").map(Number); return p.length === 3 ? p[0] * 3600 + p[1] * 60 + p[2] : p[0] * 60 + p[1]; }
  document.querySelectorAll("a.ts[data-t]").forEach(function (a) {
    var t = a.getAttribute("data-t");
    a.href = YT + "&t=" + secs(t) + "s"; a.target = "_blank"; a.rel = "noopener"; a.title = "Ouvrir la vidéo à " + t;
  });

  /* ---------- pages ---------- */
  var pages = Array.prototype.slice.call(document.querySelectorAll(".page"));
  var ids = pages.map(function (p) { return p.id; });
  var nav = document.getElementById("nav"), navm = document.getElementById("navm");
  if (nav && navm) navm.innerHTML = nav.querySelector("ol").innerHTML;
  var order = Array.prototype.slice.call(nav.querySelectorAll("li a")).map(function (a) { return a.getAttribute("href").slice(1); });
  var prev = document.getElementById("prev"), next = document.getElementById("next");
  var done = {};

  function buildToc(page) {
    var box = page.querySelector(".ptoc");
    var hs = page.querySelectorAll("h3");
    hs.forEach(function (h, i) { if (!h.id) h.id = page.id + "-s" + (i + 1); });
    if (!box || !hs.length) { if (box) box.hidden = true; return; }
    var lab = document.createElement("span"); lab.textContent = "Sur cette page"; box.appendChild(lab);
    hs.forEach(function (h) {
      var b = document.createElement("button"); b.type = "button"; b.textContent = h.textContent;
      b.addEventListener("click", function () { h.scrollIntoView({ behavior: "smooth", block: "start" }); });
      box.appendChild(b);
    });
  }

  function show(id, scroll) {
    if (ids.indexOf(id) < 0) id = "accueil";
    pages.forEach(function (p) { p.classList.toggle("on", p.id === id); });
    document.querySelectorAll(".side li a, .toc-mobile li a").forEach(function (a) { a.classList.toggle("on", a.getAttribute("href") === "#" + id); });
    var page = document.getElementById(id);
    if (!done[id]) { done[id] = true; buildToc(page); if (id !== "lexique") gloss(page); }
    var i = order.indexOf(id);
    var pv = order[i - 1], nx = order[i + 1];
    prev.hidden = !pv; next.hidden = !nx;
    if (pv) { prev.href = "#" + pv; prev.innerHTML = "<span>Page précédente</span>" + document.getElementById(pv).getAttribute("data-title"); }
    if (nx) { next.href = "#" + nx; next.innerHTML = "<span>Page suivante</span>" + document.getElementById(nx).getAttribute("data-title"); }
    var tm = document.querySelector(".toc-mobile"); if (tm) tm.open = false;
    if (scroll) window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", function () { show(location.hash.slice(1), true); });

  /* ---------- définitions au survol ---------- */
  function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
  var L = "A-Za-zÀ-ÖØ-öø-ÿ0-9";
  var terms = GLOSS.map(function (g) {
    var alts = g.m.slice().sort(function (a, b) { return b.length - a.length; }).map(esc).join("|");
    return { g: g, re: new RegExp("(^|[^" + L + "])(" + alts + ")(?=$|[^" + L + "])", g.cs ? "" : "i") };
  });
  var SKIP = /^(SVG|A|H1|H2|H3|H4|TH|SUMMARY|BUTTON|TEXTAREA|LABEL|SCRIPT|STYLE)$/;
  function skip(el) {
    for (var e = el; e && e !== document.body; e = e.parentElement) {
      if (SKIP.test(e.tagName.toUpperCase()) || (e.classList && e.classList.contains("calc-out"))) return true;
      if (e.classList && (e.classList.contains("tg") || e.classList.contains("def") || e.classList.contains("eyebrow") || e.classList.contains("map") || e.classList.contains("legend") || e.classList.contains("ptoc") || e.classList.contains("lvl"))) return true;
    }
    return false;
  }
  function gloss(page) {
    var used = {};
    var walker = document.createTreeWalker(page, NodeFilter.SHOW_TEXT, null);
    var nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (node) {
      if (!node.nodeValue.trim() || skip(node.parentElement)) return;
      var cur = node;
      var guard = 0;
      while (cur && guard++ < 20) {
        var best = null;
        terms.forEach(function (t) {
          if (used[t.g.t]) return;
          var m = t.re.exec(cur.nodeValue);
          if (m) { var idx = m.index + m[1].length; if (!best || idx < best.idx) best = { idx: idx, len: m[2].length, t: t }; }
        });
        if (!best) break;
        used[best.t.g.t] = true;
        var mid = cur.splitText(best.idx);
        var rest = mid.splitText(best.len);
        var span = document.createElement("span");
        span.className = "def"; span.tabIndex = 0;
        span.setAttribute("data-term", best.t.g.t); span.setAttribute("data-def", best.t.g.d);
        span.setAttribute("aria-label", mid.nodeValue + " : " + best.t.g.d);
        span.textContent = mid.nodeValue;
        mid.parentNode.replaceChild(span, mid);
        cur = rest;
      }
    });
  }
  var tip = document.getElementById("tip");
  function openTip(el) {
    tip.innerHTML = ""; var b = document.createElement("b"); b.textContent = el.getAttribute("data-term");
    tip.appendChild(b); tip.appendChild(document.createTextNode(el.getAttribute("data-def")));
    tip.hidden = false;
    var r = el.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight;
    var x = Math.max(8, Math.min(window.innerWidth - w - 8, r.left + r.width / 2 - w / 2));
    var y = r.top - h - 8; if (y < 8) y = r.bottom + 8;
    tip.style.left = x + "px"; tip.style.top = y + "px";
  }
  function closeTip() { tip.hidden = true; }
  document.addEventListener("mouseover", function (e) { var d = e.target.closest && e.target.closest(".def"); if (d && !d.classList.contains("demo")) openTip(d); });
  document.addEventListener("mouseout", function (e) { if (e.target.closest && e.target.closest(".def")) closeTip(); });
  document.addEventListener("focusin", function (e) { if (e.target.classList && e.target.classList.contains("def")) openTip(e.target); });
  document.addEventListener("focusout", closeTip);
  document.addEventListener("click", function (e) { var d = e.target.closest && e.target.closest(".def"); if (d && !d.classList.contains("demo")) openTip(d); else closeTip(); });
  window.addEventListener("scroll", closeTip, { passive: true });

  /* ---------- mémoire locale : cases et canevas ---------- */
  var key = "__STORE_KEY__";
  var saved = {}; try { saved = JSON.parse(localStorage.getItem(key) || "{}"); } catch (e) {}
  function save() { try { localStorage.setItem(key, JSON.stringify(saved)); } catch (e) {} }
  document.querySelectorAll(".ck input").forEach(function (i) {
    if (saved[i.id]) i.checked = true;
    i.addEventListener("change", function () { saved[i.id] = i.checked; save(); });
  });
  document.querySelectorAll(".canvas textarea").forEach(function (t) {
    if (saved[t.id]) t.value = saved[t.id];
    t.addEventListener("input", function () { saved[t.id] = t.value; save(); });
  });
  show(location.hash.slice(1), false);
})();
