/* Progressive enhancement only: the page is fully usable with JS disabled. */
(function () {
  "use strict";

  var root = document.documentElement;
  var STORAGE_KEY = "hg-theme";

  /* --- Theme toggle ----------------------------------------------------- */
  var toggle = document.querySelector("[data-theme-toggle]");

  function systemPrefersDark() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function currentlyDark() {
    var set = root.getAttribute("data-theme");
    if (set === "dark") return true;
    if (set === "light") return false;
    return systemPrefersDark();
  }

  function syncToggle() {
    if (!toggle) return;
    var dark = currentlyDark();
    toggle.setAttribute("aria-pressed", String(dark));
    var label = toggle.querySelector(".visually-hidden");
    if (label) label.textContent = dark ? "Use light theme" : "Use dark theme";
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = currentlyDark() ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try {
        localStorage.setItem(STORAGE_KEY, next);
      } catch (err) {
        /* Private mode or blocked storage: the choice just won't persist. */
      }
      syncToggle();
    });
    syncToggle();
  }

  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
    if (root.getAttribute("data-theme") === "auto") syncToggle();
  });

  /* --- Mobile navigation ------------------------------------------------ */
  var navToggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");

  if (navToggle && nav) {
    navToggle.hidden = false;
    nav.classList.add("is-collapsible");

    var setNav = function (open) {
      nav.classList.toggle("is-open", open);
      navToggle.setAttribute("aria-expanded", String(open));
    };

    navToggle.addEventListener("click", function () {
      setNav(navToggle.getAttribute("aria-expanded") !== "true");
    });

    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) setNav(false);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && navToggle.getAttribute("aria-expanded") === "true") {
        setNav(false);
        navToggle.focus();
      }
    });
  }

  /* --- Current section in the nav --------------------------------------- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.primary-nav a[href^="#"]'));
  var sections = links
    .map(function (link) { return document.querySelector(link.getAttribute("href")); })
    .filter(Boolean);

  if ("IntersectionObserver" in window && sections.length) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (link) {
          var active = link.getAttribute("href") === "#" + entry.target.id;
          if (active) {
            link.setAttribute("aria-current", "true");
          } else {
            link.removeAttribute("aria-current");
          }
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });

    sections.forEach(function (section) { observer.observe(section); });
  }

  /* --- Move focus to the section a nav link points at -------------------- */
  links.forEach(function (link) {
    link.addEventListener("click", function () {
      var target = document.querySelector(link.getAttribute("href"));
      if (target) {
        window.requestAnimationFrame(function () { target.focus({ preventScroll: true }); });
      }
    });
  });

  /* --- Footer year ------------------------------------------------------ */
  var year = document.querySelector("[data-current-year]");
  if (year) year.textContent = String(new Date().getFullYear());
})();
