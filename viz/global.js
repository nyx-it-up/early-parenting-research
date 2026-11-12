/* Helpers shared by both stories (index.html and people.html): formatting,
   tooltip, legend, data table, scroll trigger and theme toggle.
   Exposed as window.Viz. */

(function () {
  "use strict";

  // Must match the mobile breakpoint in global.css.
  const MOBILE_QUERY = "(max-width: 51.25rem), (max-height: 30rem) and (orientation: landscape)";
  const MOTION_KEY = "viz-motion";

  // The reader's choice on this site wins; otherwise follow the system setting.
  // Stored in the browser, or in the address (?motion=on) when storage is blocked.
  function savedMotion() {
    const fromAddress = new URLSearchParams(window.location.search).get("motion");
    if (fromAddress) {
      return fromAddress;
    }
    try {
      return localStorage.getItem(MOTION_KEY);
    } catch {
      return null;
    }
  }
  const REDUCED_MOTION = savedMotion()
    ? savedMotion() === "off"
    : window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.documentElement.dataset.motion = REDUCED_MOTION ? "off" : "on";
  // If the reader hasn't chosen on this site, follow a change to the system setting.
  window.matchMedia("(prefers-reduced-motion: reduce)").addEventListener("change", () => {
    if (!savedMotion()) {
      window.location.reload();
    }
  });

  const MOTION = {
    duration: REDUCED_MOTION ? 0 : 700,
    exit: REDUCED_MOTION ? 0 : 350,
    resizeDelay: 200,
  };

  const TOOLTIP = { width: 260, offsetX: 14, offsetY: 60, edge: 8 };

  const STEP_TRIGGER = {
    desktop: "-45% 0px -45% 0px",
    mobile: "-72% 0px -18% 0px",
  };

  const fmt1 = d3.format(".1f");
  const fmtInt = d3.format(",");

  function signed(value, digits = 1) {
    return `${value > 0 ? "+" : ""}${d3.format(`.${digits}f`)(value)}`;
  }

  function ciRange(ci) {
    return ci ? `${fmt1(ci[0])} to ${fmt1(ci[1])}` : "";
  }

  function ciText(ci) {
    return ci ? `95% CI ${ciRange(ci)}` : "";
  }

  function byId(id) {
    return document.getElementById(id);
  }

  function isMobile() {
    return window.matchMedia(MOBILE_QUERY).matches;
  }

  function appendSpan(parent, className, text) {
    const span = document.createElement("span");
    span.className = className;
    span.textContent = text;
    parent.appendChild(span);
    return span;
  }

  // ---------------------------------------------------------------- resize

  const redrawOnResize = [];
  let resizeTimer = null;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => redrawOnResize.forEach((redraw) => redraw()), MOTION.resizeDelay);
  });

  function onResize(redraw) {
    redrawOnResize.push(redraw);
  }

  // ---------------------------------------------------------------- tooltip

  const tooltip = byId("tooltip");

  // Text is rewritten only when the mark changes, so screen readers announce it once.
  let tooltipText = "";

  function showTooltip(event, value, label) {
    const text = `${value}|${label}`;
    if (text !== tooltipText) {
      tooltipText = text;
      tooltip.textContent = "";
      appendSpan(tooltip, "tt-value", value);
      appendSpan(tooltip, "tt-label", label);
    }
    let x = event.clientX;
    let y = event.clientY;
    if (x === undefined || event.type === "focus") {
      const box = event.target.getBoundingClientRect();
      x = box.left + box.width / 2;
      y = box.top;
    }
    tooltip.style.left = `${Math.min(x + TOOLTIP.offsetX, window.innerWidth - TOOLTIP.width - TOOLTIP.edge)}px`;
    tooltip.style.top = `${Math.max(y - TOOLTIP.offsetY, TOOLTIP.edge)}px`;
    tooltip.style.opacity = 1;
  }

  function hideTooltip() {
    tooltipText = "";
    tooltip.style.opacity = 0;
  }

  // focusable = false for marks too numerous to tab through (the data table covers them).
  function attachTooltip(selection, valueFn, labelFn, focusable = true) {
    if (focusable) {
      selection
        .attr("tabindex", 0)
        .attr("role", "img")
        .attr("aria-label", (d) => `${labelFn(d)}: ${valueFn(d)}`);
    }
    selection
      .on("pointerenter pointermove focus click", (event, d) => showTooltip(event, valueFn(d), labelFn(d)))
      .on("pointerleave blur", hideTooltip);
  }

  // ------------------------------------------------------- legend and table

  function legend(elementId, items) {
    const box = byId(elementId);
    box.textContent = "";
    for (const item of items) {
      const entry = appendSpan(box, "legend-item", "");
      const swatch = appendSpan(entry, item.shape === "rect" ? "swatch-rect" : "swatch-dot", "");
      swatch.style.background = item.color;
      if (item.outline) {
        swatch.style.boxShadow = `inset 0 0 0 0.125rem ${item.outline}`;
      }
      appendSpan(entry, "", item.label);
    }
  }

  const COLUMN = {
    pct: (label = "%") => ({ label, value: (r) => fmt1(r.pct) }),
    ci: (label = "95% CI") => ({ label, value: (r) => ciRange(r.ci) }),
    n: (label = "n") => ({ label, value: (r) => fmtInt(r.n) }),
    field: (label, key) => ({ label, value: (r) => r[key] }),
  };

  function table(elementId, columns, rows) {
    const box = byId(elementId);
    box.textContent = "";
    const tableEl = document.createElement("table");
    // The box scrolls sideways when the table is wider, so it must be reachable by keyboard.
    // It and the table are named by the chart's title (by reference, so a title set later counts).
    const title = box.closest("figure, section")?.querySelector(".figure-title, h2");
    box.classList.add("table-scroll");
    box.tabIndex = 0;
    box.setAttribute("role", "region");
    if (title) {
      title.id = title.id || `${elementId}-title`;
      box.setAttribute("aria-labelledby", title.id);
      tableEl.setAttribute("aria-labelledby", title.id);
    } else {
      box.setAttribute("aria-label", "Data table");
    }
    const head = tableEl.createTHead().insertRow();
    for (const column of columns) {
      const th = head.appendChild(document.createElement("th"));
      th.scope = "col";
      th.textContent = column.label;
    }
    const body = tableEl.createTBody();
    for (const row of rows) {
      const tr = body.insertRow();
      for (const column of columns) {
        tr.insertCell().textContent = column.value(row);
      }
    }
    box.appendChild(tableEl);
  }

  // ---------------------------------------------------------- scroll trigger

  function onSteps(sectionId, update) {
    const steps = document.querySelectorAll(`#${sectionId} .step`);
    let observer = null;
    // On phones the trigger sits low, so the active card stays below the pinned graphic.
    // Rebuilt when the window crosses the phone breakpoint (rotating, resizing).
    function watch() {
      if (observer) {
        observer.disconnect();
      }
      observer = new IntersectionObserver((entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            steps.forEach((s) => s.classList.toggle("is-active", s === entry.target));
            update(Array.prototype.indexOf.call(steps, entry.target));
          }
        }
      }, { rootMargin: isMobile() ? STEP_TRIGGER.mobile : STEP_TRIGGER.desktop });
      steps.forEach((s) => observer.observe(s));
    }
    window.matchMedia(MOBILE_QUERY).addEventListener("change", watch);
    watch();
    update(0);
  }

  // ------------------------------------------------------------ theme toggle

  function initThemeToggle(buttonId) {
    const toggle = byId(buttonId);
    toggle.removeAttribute("aria-label"); // the visible text is the name
    const currentTheme = () => document.documentElement.dataset.theme
      || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    const label = () => {
      toggle.textContent = currentTheme() === "dark" ? "Light mode" : "Dark mode";
    };
    const announce = () => document.dispatchEvent(new CustomEvent("themechange"));
    toggle.addEventListener("click", () => {
      document.documentElement.dataset.theme = currentTheme() === "dark" ? "light" : "dark";
      label();
      announce();
    });
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
      label();
      announce();
    });
    label();
    initMotionToggle(toggle);
  }

  // A second switch beside the theme toggle. Changing it reloads the page.
  function initMotionToggle(themeButton) {
    const group = document.createElement("div");
    group.className = "page-toggles";
    themeButton.replaceWith(group);
    const motion = document.createElement("button");
    motion.type = "button";
    motion.className = "pill";
    motion.textContent = REDUCED_MOTION ? "Motion: off" : "Motion: on";
    motion.addEventListener("click", () => {
      const next = REDUCED_MOTION ? "on" : "off";
      const url = new URL(window.location.href);
      try {
        localStorage.setItem(MOTION_KEY, next);
        url.searchParams.delete("motion");
      } catch {
        url.searchParams.set("motion", next);
      }
      window.location.replace(url);
    });
    group.append(motion, themeButton);
  }

  window.Viz = {
    MOTION, REDUCED_MOTION,
    fmt1, fmtInt, signed, ciRange, ciText,
    byId, isMobile, onResize,
    showTooltip, hideTooltip, attachTooltip,
    legend, table, COLUMN,
    onSteps, initThemeToggle,
  };
})();
