(function () {
  "use strict";

  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------------------------
     i18n
     --------------------------------------------------------------------- */
  var LANG_KEY = "axis-lang";

  function getPath(obj, path) {
    return path.split(".").reduce(function (acc, key) {
      return acc && acc[key] !== undefined ? acc[key] : undefined;
    }, obj);
  }

  function applyLang(lang) {
    var dict = window.AXIS_I18N && window.AXIS_I18N[lang];
    if (!dict) return;

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var value = getPath(dict, el.getAttribute("data-i18n"));
      if (typeof value === "string") el.textContent = value;
    });

    document.documentElement.setAttribute("lang", lang);
    document.querySelectorAll(".lang-btn").forEach(function (btn) {
      var active = btn.getAttribute("data-lang") === lang;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", String(active));
    });

    try { localStorage.setItem(LANG_KEY, lang); } catch (e) { /* storage unavailable */ }
  }

  function initLang() {
    var stored = null;
    try { stored = localStorage.getItem(LANG_KEY); } catch (e) { /* ignore */ }
    var lang = stored === "en" ? "en" : "fr";
    if (lang !== "fr") applyLang(lang);

    document.querySelectorAll(".lang-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        applyLang(btn.getAttribute("data-lang"));
      });
    });
  }

  /* ---------------------------------------------------------------------
     Navigation: floating state, scroll shrink, mobile menu
     --------------------------------------------------------------------- */
  function initNav() {
    var nav = document.getElementById("site-nav");
    var burger = document.querySelector(".nav-burger");
    var mobileMenu = document.getElementById("mobile-menu");

    requestAnimationFrame(function () {
      nav.classList.add("is-ready");
    });

    var lastY = window.scrollY;
    function onScroll() {
      nav.classList.toggle("is-scrolled", window.scrollY > 40);
      lastY = window.scrollY;
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    function closeMenu() {
      mobileMenu.classList.remove("is-open");
      burger.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    }
    function openMenu() {
      mobileMenu.classList.add("is-open");
      burger.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
    }

    burger.addEventListener("click", function () {
      var isOpen = mobileMenu.classList.contains("is-open");
      if (isOpen) closeMenu(); else openMenu();
    });
    mobileMenu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeMenu);
    });
    window.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });
  }

  /* ---------------------------------------------------------------------
     Hero entrance
     --------------------------------------------------------------------- */
  function initHero() {
    var hero = document.querySelector(".hero");
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        hero.classList.add("is-ready");
      });
    });
  }

  /* ---------------------------------------------------------------------
     Scroll reveal (IntersectionObserver — cheap, no scroll listeners)
     --------------------------------------------------------------------- */
  function initReveal() {
    var items = document.querySelectorAll(".reveal-on-scroll, .split-bar, .problem-visual");
    if (!("IntersectionObserver" in window) || prefersReducedMotion) {
      items.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -60px 0px" }
    );
    items.forEach(function (el, i) {
      el.style.transitionDelay = prefersReducedMotion ? "0s" : (Math.min(i % 6, 5) * 0.06) + "s";
      observer.observe(el);
    });
  }

  /* ---------------------------------------------------------------------
     Animated counters (dataset / evaluation numbers)
     --------------------------------------------------------------------- */
  function animateCount(el) {
    var target = parseFloat(el.getAttribute("data-count-to"));
    var decimals = parseInt(el.getAttribute("data-decimals") || "0", 10);
    if (prefersReducedMotion || isNaN(target)) {
      el.textContent = formatNumber(target, decimals);
      return;
    }
    var duration = 1600;
    var start = null;

    function step(ts) {
      if (start === null) start = ts;
      var progress = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = formatNumber(target * eased, decimals);
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function formatNumber(value, decimals) {
    var fixed = value.toFixed(decimals);
    var parts = fixed.split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    return parts.join(",");
  }

  function initCounters() {
    var counters = document.querySelectorAll("[data-count-to]");
    if (!("IntersectionObserver" in window)) {
      counters.forEach(animateCount);
      return;
    }
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCount(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach(function (el) { observer.observe(el); });
  }

  /* ---------------------------------------------------------------------
     Hero indicator cycling (01 / 02 / 03)
     --------------------------------------------------------------------- */
  function initIndicator() {
    var items = document.querySelectorAll(".ind-item");
    if (!items.length || prefersReducedMotion) return;
    var i = 0;
    setInterval(function () {
      items[i].classList.remove("is-active");
      i = (i + 1) % items.length;
      items[i].classList.add("is-active");
    }, 6000);
  }

  /* ---------------------------------------------------------------------
     Subtle desktop parallax on the hero visual (transform only, GPU-friendly)
     --------------------------------------------------------------------- */
  function initParallax() {
    if (prefersReducedMotion || window.matchMedia("(max-width: 1024px)").matches) return;
    var visual = document.getElementById("hero-visual");
    if (!visual) return;
    var building = visual.querySelector(".axo-building");
    var annos = visual.querySelectorAll(".anno");
    var card = visual.querySelector(".hero-card");
    var ticking = false;
    var mx = 0, my = 0;

    window.addEventListener("mousemove", function (e) {
      var rect = visual.getBoundingClientRect();
      mx = ((e.clientX - rect.left) / rect.width - 0.5);
      my = ((e.clientY - rect.top) / rect.height - 0.5);
      if (!ticking) {
        requestAnimationFrame(update);
        ticking = true;
      }
    }, { passive: true });

    function update() {
      building.style.transform = "translate3d(" + (mx * -6) + "px," + (my * -6) + "px,0)";
      annos.forEach(function (a, i) {
        var depth = 10 + i * 2;
        a.style.transform = "translate(-50%, -50%) translate3d(" + (mx * depth) + "px," + (my * depth) + "px,0)";
      });
      if (card) card.style.transform = "translate3d(" + (mx * 4) + "px," + (my * 4) + "px,0)";
      ticking = false;
    }
  }

  /* ---------------------------------------------------------------------
     Boot
     --------------------------------------------------------------------- */
  document.addEventListener("DOMContentLoaded", function () {
    initLang();
    initNav();
    initHero();
    initReveal();
    initCounters();
    initIndicator();
    initParallax();
  });
})();
