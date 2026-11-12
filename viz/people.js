/* The Room: every parent who answered the NSCH (2023-2025), one circle each.
   Data: window.RESPONDENTS (viz/respondents.js). Circles are respondents;
   every percentage shown uses the survey weights, as in the analysis.
   The circles are drawn on <canvas> (over 130,000 of them), straight into a
   pixel buffer; between steps every circle travels to its new place. */

(function () {
  "use strict";

  // ================================================================ settings

  const {
    REDUCED_MOTION, fmtInt, byId, isMobile, onResize,
    showTooltip, hideTooltip, table, onSteps, initThemeToggle,
  } = window.Viz;

  const YEARS = [2023, 2024, 2025];
  const EMPLOYMENT = ["Full-time", "Part-time", "Looking for work", "Not looking for work"];
  const BANDS = ["0-5", "6-11", "12-17"];
  const BAND_TEXT = { "0-5": "under 6", "6-11": "6 to 11", "12-17": "12 to 17" };
  const AGE_CHOICES = [
    { key: "baby", label: "Under 2", text: "under 2", test: (p) => p.age < 2 },
    { key: "0-5", label: "Under 6", text: "under 6", test: (p) => p.band === "0-5" },
    { key: "6-11", label: "6 to 11", text: "6 to 11", test: (p) => p.band === "6-11" },
    { key: "12-17", label: "12 to 17", text: "12 to 17", test: (p) => p.band === "12-17" },
  ];
  const SHORT_GROUP = {
    "Full-time": "Full-time", "Part-time": "Part-time",
    "Looking for work": "Looking", "Not looking for work": "Not looking",
  };
  const WORK_TEXT = {
    "Full-time": { one: "works full-time", many: "work full-time" },
    "Part-time": { one: "works part-time", many: "work part-time" },
    "Looking for work": { one: "is looking for work", many: "are looking for work" },
    "Not looking for work": { one: "is not employed and not looking", many: "are not employed and not looking" },
  };
  const PARENT = {
    mothers: { one: "mother", many: "mothers", title: "Mothers" },
    fathers: { one: "father", many: "fathers", title: "Fathers" },
  };
  const RATING_TEXT = { 1: "Excellent", 2: "Very good", 3: "Good", 4: "Fair", 5: "Poor" };

  // Ratings drawn from the center of each disc outward: excellent first, poor at the rim.
  const TONES = [1, 2, 3, 4, 5];
  const LEGEND_ORDER = [1, 2, 3, 4, 5];
  const NEUTRAL_COLOR = "--person-none";
  const RING_COLOR = "--person-focus-ring";
  const COLORS = [NEUTRAL_COLOR, "--rating-1", "--rating-2", "--rating-3", "--rating-4", "--rating-5"];

  const CANVAS = {
    circleFrom: 4, // device px: smaller dots are drawn as squares
    masks: 48, // circle masks kept for reuse, newest first
    splatBelow: 4, // device px: smaller cells are drawn as a full cell, antialiased by coverage
    dimmed: 0.14, // opacity of dots out of focus
  };

  const MIN_N = 30; // NSCH reliability rule: do not report groups under 30 respondents

  const LAYOUT = {
    region: {
      desktop: { x0: 0.37, x1: 0.98, y0: 0.08, y1: 0.9 },
      mobile: { x0: 0.03, x1: 0.97, y0: 0.15, y1: 0.9 }, // leaves room for the view and zoom controls
    },
    gap: 26,
    gapMobile: 12,
    nameBand: 34,
    countBand: 18,
    headerBand: 28,
    rowHeaderWidth: 96,
    columnGap: 4, // between rating columns within a year
    yearBand: 26, // space under the columns for the year labels
    stackGap: 6, // between the mothers and fathers column of one group
    stackTop: 40, // space above the stacks for the group name and shares
    spacing: { min: 0.2, max: 16, searchSteps: 30 },
    dotShare: 0.42, // dot radius as a share of the spacing
    resizeShare: 0.15, // on phones, height changes smaller than this share keep the layout
  };

  // Room around every piece of text, in px: labels, zoom strip, legend, cards.
  const TEXT = {
    pad: 4, // between two labels
    gap: 12, // between text and the area the dots use
    line: 18, // a label's name above its count
    nameChar: 8.4, // estimated width of one character of a cluster name
    countChar: 7.2, // estimated width of one character of a count
  };

  const PIZZA = {
    start: -Math.PI / 2, // first slice starts at twelve o'clock
    gap: 0.7, // half the width of the cut between slices, in dot spacings
    labelBand: 30, // room outside the crust for the year labels
  };

  const TRICKLE = {
    total: 3500, // ms from the first dot leaving to the last dot landing
    flight: 700, // ms each dot travels
    bend: 0.2, // how far a path curves, as a share of its length
  };

  const ZOOM = {
    max: 40, // largest zoom factor
    step: 1.6, // zoom factor of the + and − buttons
    glide: 600, // ms for button and double-click zooms
    pad: 24, // px of room around a piece zoomed to by double-click
    hint: "Ctrl + scroll or pinch to zoom · drag to move · double-click a group",
    keys: "Dots of this view. Arrow keys move, plus and minus zoom, 0 shows everything, Enter zooms to the next group.",
    keyStep: 60, // px an arrow key moves the view
    hintTouch: "Pinch to zoom · double-tap a group",
  };

  const HOVER = { reach: 1.6, minReach: 6, ring: 3, tapSlop: 10 };
  const NEAR_VIEWPORT = "10% 0px"; // draw a room only when it is this close
  const GOLDEN_ANGLE = Math.PI * (3 - Math.sqrt(5));

  // ================================================================ people

  function decode(raw, parent) {
    const people = [];
    for (let i = 0; i < raw.rating.length; i += 1) {
      const age = parseInt(raw.age[i], 36);
      people.push({
        parent,
        group: EMPLOYMENT[Number(raw.employment[i])],
        age,
        band: age <= 5 ? "0-5" : age <= 11 ? "6-11" : "12-17",
        rating: Number(raw.rating[i]),
        year: 2020 + Number(raw.year[i]),
        weight: raw.weight[i],
        order: i,
      });
    }
    return people;
  }

  const mothers = decode(window.RESPONDENTS.mothers, "mothers");
  const fathers = decode(window.RESPONDENTS.fathers, "fathers");

  // Weighted percentage of people passing test, and the respondent count.
  function weighted(people, test) {
    let total = 0;
    let hit = 0;
    for (const p of people) {
      total += p.weight;
      if (test(p)) {
        hit += p.weight;
      }
    }
    return { pct: total ? (100 * hit) / total : NaN, n: people.length };
  }

  const fairOrPoor = (p) => p.rating >= 4;
  const highRating = (p) => p.rating <= 2;
  const fpOf = (people) => Math.round(weighted(people, fairOrPoor).pct);
  const inGroup = (people, group) => people.filter((p) => p.group === group);

  const STATS = {
    mothersCount: fmtInt(mothers.length),
    fathersCount: fmtInt(fathers.length),
    mothersFp: fpOf(mothers),
    fathersFp: fpOf(fathers),
    fullTimeFp: fpOf(inGroup(mothers, "Full-time")),
    lookingFp: fpOf(inGroup(mothers, "Looking for work")),
    notLookingYoungFp: fpOf(inGroup(mothers, "Not looking for work").filter((p) => p.band === "0-5")),
    fullTimeHigh: Math.round(weighted(inGroup(mothers, "Full-time"), (p) => p.rating <= 2).pct),
    lookingHigh: Math.round(weighted(inGroup(mothers, "Looking for work"), (p) => p.rating <= 2).pct),
    notLookingHigh: Math.round(weighted(inGroup(mothers, "Not looking for work"), (p) => p.rating <= 2).pct),
    notLookingFp: fpOf(inGroup(mothers, "Not looking for work")),
    notLookingTeenFp: fpOf(inGroup(mothers, "Not looking for work").filter((p) => p.band === "12-17")),
    babyCount: fmtInt(mothers.filter((p) => p.age < 2).length),
    babyFullTimeFp: fpOf(inGroup(mothers, "Full-time").filter((p) => p.age < 2)),
    babyLookingFp: fpOf(inGroup(mothers, "Looking for work").filter((p) => p.age < 2)),
    fathersFullTimeFp: fpOf(inGroup(fathers, "Full-time")),
    fathersLookingFp: fpOf(inGroup(fathers, "Looking for work")),
    fathersNotLookingFp: fpOf(inGroup(fathers, "Not looking for work")),
  };
  for (const span of document.querySelectorAll("[data-stat]")) {
    span.textContent = STATS[span.dataset.stat];
  }

  // ================================================================ room

  /* A room draws a population of circles on a canvas and moves them between
     views. view: {parent, filter, grid: {cols, rows, colOf, rowOf, rowName},
     groupBy, names, order, colors, sorted, counts, focus, summary} */
  function createRoom(sectionId, people) {
    const population = people.map((person) => ({ ...person })); // this room's own positions
    const section = byId(sectionId);
    const canvas = section.querySelector(".room-canvas");
    const stage = section.querySelector(".room-stage");
    const labels = d3.select(section.querySelector(".room-labels"));
    const summary = section.querySelector(".room-summary");
    const legendBox = section.querySelector(".room-legend");
    const size = { width: 0, height: 0 };
    let zoomNow = d3.zoomIdentity;
    let dot = 1;
    let reach = HOVER.minReach;
    let current = null;
    let finder = null;
    function measure() {
      size.width = canvas.offsetWidth;
      size.height = canvas.offsetHeight;
      sizeCanvas();
    }

    /* The part of the stage the dots may use: clear of the step cards on the
       left, the zoom strip at the top and the legend at the bottom. */
    let bounds = null;

    function measureRegion() {
      const share = isMobile() ? LAYOUT.region.mobile : LAYOUT.region.desktop;
      const stageBox = stage.getBoundingClientRect();
      const zoomControls = stage.querySelector(".zoom-controls");
      const switchBox = stage.querySelector(".view-switch").getBoundingClientRect();
      const rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
      zoomControls.style.top = isMobile() ? `${(switchBox.bottom - stageBox.top + TEXT.pad) / rem}rem` : "";
      const zoomBox = zoomControls.getBoundingClientRect();
      const legend = legendBox.getBoundingClientRect();
      const cards = section.querySelector(".room-steps").getBoundingClientRect();
      const beside = !isMobile();
      bounds = {
        x0: Math.max(share.x0 * size.width, beside ? cards.right - stageBox.left + TEXT.gap : 0),
        x1: share.x1 * size.width,
        y0: Math.max(share.y0 * size.height, zoomBox.bottom - stageBox.top + TEXT.gap),
        y1: Math.min(share.y1 * size.height, legend.top - stageBox.top - TEXT.gap),
      };
    }

    function region() {
      if (!bounds) {
        measureRegion();
      }
      return bounds;
    }

    // ---------------------------------------------------------- layout

    const discRadius = (n, spacing) => spacing * Math.sqrt(n / Math.PI) + spacing;

    const shortOnMobile = (name) => (isMobile() ? SHORT_GROUP[name] || name : name);

    function buildClusters(view) {
      const visible = population.filter(view.filter || (() => true));
      const split = view.columns || view.stacks;
      const keyOf = split
        ? (p) => `${split.groupOf(p)}|${split.subOf(p)}`
        : view.grid
          ? (p) => `${view.grid.colOf(p)}|${view.grid.rowOf(p)}`
          : view.groupBy || (() => "all");
      const clusters = d3.groups(visible, keyOf).map(([key, members]) => {
        const first = members[0];
        return {
          key,
          members,
          name: view.names ? shortOnMobile(view.groupBy(first)) : "",
          col: view.grid ? view.grid.colOf(first) : null,
          row: view.grid ? view.grid.rowOf(first) : null,
          group: split ? split.groupOf(first) : null,
          sub: split ? split.subOf(first) : null,
          focus: !view.focus || view.focus(first),
        };
      });
      if (view.order) {
        clusters.sort((a, b) => view.order.indexOf(a.key) - view.order.indexOf(b.key));
      }
      for (const cluster of clusters) {
        cluster.members.sort(view.sorted
          ? (a, b) => TONES.indexOf(a.rating) - TONES.indexOf(b.rating) || a.order - b.order
          : (a, b) => a.order - b.order);
      }
      return clusters;
    }

    // Each member's place (ox, oy) relative to its cluster's anchor (x, y).
    function sunflower(c, spacing) {
      c.members.forEach((p, i) => {
        const radius = spacing * Math.sqrt((i + 0.5) / Math.PI);
        const angle = i * GOLDEN_ANGLE;
        p.ox = radius * Math.cos(angle);
        p.oy = radius * Math.sin(angle);
      });
    }

    // Rows of perRow dots filled from the bottom-left corner up.
    function stackRows(c, spacing, perRow, rowStep = spacing) {
      c.members.forEach((p, i) => {
        p.ox = (i % perRow) * spacing + spacing / 2;
        p.oy = -Math.floor(i / perRow) * rowStep - rowStep / 2;
      });
    }

    // Estimated width of a cluster's label (name above count), with padding.
    function labelWidth(c, view, twoLines) {
      const name = c.name.length * TEXT.nameChar;
      const counted = view.counts ? Math.max(...countLines(c.members, twoLines).map((line) => line.length)) * TEXT.countChar : 0;
      return Math.max(name, counted) + 2 * TEXT.pad;
    }

    // Place cluster centers for a given spacing; return false if they don't fit.
    // Rows of perRow clusters each: all in one row, two rows of half, or one per row.
    const rowChoices = (n) => [...new Set([n, Math.ceil(n / 2), 1])];

    function placeRows(clusters, spacing, area, view, perRow) {
      const labelBand = (view.names ? LAYOUT.nameBand : 0) + (view.counts ? LAYOUT.countBand * (isMobile() ? 2 : 1) : 0);
      for (const c of clusters) {
        c.r = discRadius(c.members.length, spacing);
        c.w = Math.max(2 * c.r, labelBand ? labelWidth(c, view, isMobile()) : 0);
      }
      const rows = d3.range(0, clusters.length, perRow).map((start) => clusters.slice(start, start + perRow));
      const heights = rows.map((row) => 2 * d3.max(row, (c) => c.r) + labelBand);
      const totalHeight = d3.sum(heights) + LAYOUT.gap * (rows.length - 1);
      const widest = d3.max(rows, (row) => d3.sum(row, (c) => c.w) + LAYOUT.gap * (row.length - 1));
      let y = area.y0 + Math.max(0, (area.y1 - area.y0 - totalHeight) / 2);
      rows.forEach((row, i) => {
        const rowWidth = d3.sum(row, (c) => c.w) + LAYOUT.gap * (row.length - 1);
        let x = area.x0 + (area.x1 - area.x0 - rowWidth) / 2;
        for (const c of row) {
          c.x = x + c.w / 2;
          c.y = y + labelBand + (heights[i] - labelBand) / 2;
          x += c.w + LAYOUT.gap;
        }
        y += heights[i] + LAYOUT.gap;
      });
      return totalHeight <= area.y1 - area.y0 && widest <= area.x1 - area.x0;
    }

    function placeGrid(clusters, spacing, area, view) {
      const grid = view.grid;
      const labelsIn = (col, twoLines) => Math.max(0, ...clusters.filter((c) => c.col === col).map((c) => labelWidth(c, view, twoLines)));
      const wideLabels = LAYOUT.rowHeaderWidth + d3.sum(grid.cols, (col) => (view.counts ? labelsIn(col, false) : 0)) + LAYOUT.gap * (grid.cols.length - 1);
      const compact = isMobile() || wideLabels > area.x1 - area.x0;
      const countBand = view.counts && !isMobile() ? LAYOUT.countBand * (compact ? 2 : 1) : 0;
      const rowHeaderWidth = compact ? 0 : LAYOUT.rowHeaderWidth;
      const rowHeaderBand = compact ? LAYOUT.headerBand : 0;
      for (const c of clusters) {
        c.r = discRadius(c.members.length, spacing);
      }
      const widest = (test) => Math.max(0, ...clusters.filter(test).map((c) => 2 * c.r));
      const colWidth = grid.cols.map((col) => Math.max(widest((c) => c.col === col), countBand ? labelsIn(col, compact) : 0));
      const rowHeight = grid.rows.map((row) => widest((c) => c.row === row) + countBand + rowHeaderBand);
      const gap = compact ? LAYOUT.gapMobile : LAYOUT.gap;
      const width = rowHeaderWidth + d3.sum(colWidth) + gap * (grid.cols.length - 1);
      const height = LAYOUT.headerBand + d3.sum(rowHeight) + gap * (grid.rows.length - 1);
      grid.left = area.x0 + (area.x1 - area.x0 - width) / 2;
      grid.top = area.y0 + Math.max(0, (area.y1 - area.y0 - height) / 2);
      grid.compact = compact;
      grid.colX = [];
      let x = grid.left + rowHeaderWidth;
      colWidth.forEach((w) => {
        grid.colX.push(x + w / 2);
        x += w + gap;
      });
      grid.rowTop = [];
      grid.rowY = [];
      let y = grid.top + LAYOUT.headerBand;
      rowHeight.forEach((h) => {
        grid.rowTop.push(y);
        grid.rowY.push(y + rowHeaderBand + countBand + (h - rowHeaderBand - countBand) / 2);
        y += h + gap;
      });
      for (const c of clusters) {
        c.x = grid.colX[grid.cols.indexOf(c.col)];
        c.y = grid.rowY[grid.rows.indexOf(c.row)];
      }
      return width <= area.x1 - area.x0 && height <= area.y1 - area.y0;
    }

    // Equal-width columns side by side, in groups: where each column starts.
    function columnSlots(area, groupCount, subCount, gapInside) {
      const free = area.x1 - area.x0 - LAYOUT.gap * (groupCount - 1) - gapInside * (subCount - 1) * groupCount;
      const width = free / (groupCount * subCount);
      const groupWidth = subCount * (width + gapInside) - gapInside;
      const left = (g, k) => area.x0 + g * (groupWidth + LAYOUT.gap) + k * (width + gapInside);
      const middle = (g) => left(g, 0) + groupWidth / 2;
      return { width, left, middle };
    }

    /* Column chart of dots: one group of columns per year, one column per rating.
       Each column is a block of dots filled from the bottom, the same width for all. */
    function placeColumns(clusters, spacing, area, view) {
      const { groups, subs } = view.columns;
      const slots = columnSlots(area, groups.length, subs.length, LAYOUT.columnGap);
      const perRow = Math.max(1, Math.floor(slots.width / spacing));
      const base = area.y1 - LAYOUT.yearBand;
      let tallest = 0;
      view.columns.groupX = groups.map((group, g) => slots.middle(g));
      view.columns.base = base;
      for (const c of clusters) {
        c.x = slots.left(groups.indexOf(c.group), subs.indexOf(c.sub)) + (slots.width - perRow * spacing) / 2;
        c.y = base;
        c.perRow = perRow;
        tallest = Math.max(tallest, Math.ceil(c.members.length / perRow) * spacing);
      }
      return tallest <= base - area.y0;
    }

    /* 100% stacked columns: every column has the same height and width, so each
       column gets its own dot spacing: as many dots per row as keeps them about
       square, rows stretched a little so the last row reaches the top. */
    function placeStacks(clusters, area, view) {
      const { groups, subs } = view.stacks;
      const slots = columnSlots(area, groups.length, subs.length, LAYOUT.stackGap);
      const base = area.y1 - LAYOUT.yearBand;
      const height = base - area.y0 - LAYOUT.stackTop;
      Object.assign(view.stacks, { base, top: base - height, groupX: groups.map((group, g) => slots.middle(g)) });
      for (const c of clusters) {
        const n = c.members.length;
        const perRow = Math.max(1, Math.round(Math.sqrt((n * slots.width) / height)));
        c.perRow = perRow;
        c.rowStep = height / Math.ceil(n / perRow);
        c.spacing = Math.min(slots.width / perRow, c.rowStep);
        c.x = slots.left(groups.indexOf(c.group), subs.indexOf(c.sub));
        c.y = base;
        c.mid = c.x + slots.width / 2;
      }
    }

    /* One disc cut into slices, one per survey year, each slice's angle in
       proportion to its count. Inside a slice, dots fill arcs of a polar grid
       from the center out, so the ratings form rings: excellent in the middle,
       poor at the crust. A thin cut is kept clear between slices. */
    function placePizza(clusters, spacing, area, view, final) {
      const c = clusters[0];
      const { slices, sliceOf } = view.pizza;
      const cut = PIZZA.gap * spacing;
      let angle = PIZZA.start;
      let crust = 0;
      view.pizza.edges = [];
      c.bySlice = c.bySlice || d3.group(c.members, sliceOf);
      for (const slice of slices) {
        const members = c.bySlice.get(slice) || [];
        const a0 = angle;
        const a1 = angle + (2 * Math.PI * members.length) / c.members.length;
        let placed = 0;
        for (let ring = 0; placed < members.length; ring += 1) {
          const r = (ring + 0.5) * spacing;
          const open = a1 - a0 - 2 * Math.asin(Math.min(1, cut / r));
          const take = Math.min(open > 0 ? Math.floor((open * r) / spacing) : 0, members.length - placed);
          for (let k = 0; final && k < take; k += 1) {
            const phi = (a0 + a1) / 2 - open / 2 + (open * (k + 0.5)) / take;
            const p = members[placed + k];
            p.ox = r * Math.cos(phi);
            p.oy = r * Math.sin(phi);
          }
          placed += take;
          crust = Math.max(crust, r + spacing / 2);
        }
        view.pizza.edges.push({ slice, mid: (a0 + a1) / 2 });
        angle = a1;
      }
      c.r = crust;
      c.x = (area.x0 + area.x1) / 2;
      c.y = (area.y0 + area.y1) / 2;
      view.pizza.crust = crust;
      const reach = 2 * (crust + PIZZA.labelBand);
      return reach <= area.x1 - area.x0 && reach <= area.y1 - area.y0;
    }

    // Largest spacing at which everything fits: the same spacing for every circle.
    function fitSpacing(clusters, view) {
      const area = region();
      if (view.stacks) {
        placeStacks(clusters, area, view);
        return d3.min(clusters, (c) => c.spacing);
      }
      const place = (s, final) => {
        if (view.pizza) {
          return placePizza(clusters, s, area, view, final);
        }
        if (view.columns) {
          return placeColumns(clusters, s, area, view);
        }
        return view.grid ? placeGrid(clusters, s, area, view) : placeRows(clusters, s, area, view, perRow);
      };
      let perRow = clusters.length;
      const search = () => {
        let low = LAYOUT.spacing.min;
        let high = LAYOUT.spacing.max;
        for (let i = 0; i < LAYOUT.spacing.searchSteps; i += 1) {
          const mid = (low + high) / 2;
          if (place(mid)) {
            low = mid;
          } else {
            high = mid;
          }
        }
        return low;
      };
      let best = { spacing: -1, perRow };
      for (const choice of view.pizza || view.columns || view.grid ? [perRow] : rowChoices(clusters.length)) {
        perRow = choice;
        const spacing = search();
        if (spacing > best.spacing) {
          best = { spacing, perRow };
        }
      }
      perRow = best.perRow;
      place(best.spacing, true);
      return best.spacing;
    }

    const dotSize = (spacing) => 2 * Math.max(0.6, spacing * LAYOUT.dotShare);

    // Final places; rank (0 = lands first) fills each cluster center-out or bottom-up.
    function setTargets(clusters, spacing, view) {
      population.forEach((p) => {
        p.visible = false;
      });
      for (const c of clusters) {
        const s = c.spacing || spacing;
        if (c.rowStep) {
          stackRows(c, (c.mid - c.x) * 2 / c.perRow, c.perRow, c.rowStep);
        } else if (c.perRow) {
          stackRows(c, s, c.perRow);
        } else if (!view.pizza) {
          sunflower(c, s);
        }
        c.members.forEach((p, i) => {
          p.tx = c.x + p.ox;
          p.ty = c.y + p.oy;
          p.w = c.rowStep ? ((c.mid - c.x) * 2) / c.perRow : s;
          p.h = c.rowStep || s;
          p.rank = i / c.members.length;
          p.visible = true;
          p.dimmed = !c.focus;
        });
      }
    }

    // ---------------------------------------------------------- drawing

    /* Every dot lives in typed arrays: where it starts (x0, y0) and ends
       (x1, y1), its size, color, delay and bend. One requestAnimationFrame
       loop moves the dots and writes them straight into a pixel buffer, which
       is put on the canvas in one call. Small dots are pixel-aligned squares;
       larger ones use a cached circle mask. */
    const count = population.length;
    const X0 = new Float32Array(count);
    const Y0 = new Float32Array(count);
    const X1 = new Float32Array(count);
    const Y1 = new Float32Array(count);
    const W = new Float32Array(count);
    const H = new Float32Array(count);
    const DELAY = new Float32Array(count);
    const BEND = new Float32Array(count);
    const COLOR = new Uint8Array(count);
    const SHOWN = new Uint8Array(count);
    const SQUARE = Uint8Array.from(population, (p) => (p.parent === "fathers" ? 1 : 0));
    const ctx = canvas.getContext("2d");
    const ringCanvas = document.createElement("canvas");
    ringCanvas.className = "room-ring";
    ringCanvas.setAttribute("aria-hidden", "true");
    canvas.after(ringCanvas);
    const ringCtx = ringCanvas.getContext("2d");
    const palette = new Uint32Array(2 * COLORS.length);
    let ringColor = "";
    const masks = new Map();
    let pixels = null;
    let buffer = null;
    let dpr = 1;
    let hovered = null;
    let motion = null; // { start, flight } while dots travel
    let frame = 0;

    function readColors() {
      const probe = document.createElement("span");
      stage.appendChild(probe);
      const pack = (name, alpha) => {
        probe.style.color = `var(${name})`;
        const [r, g, b] = getComputedStyle(probe).color.match(/\d+/g).map(Number);
        return ((alpha << 24) | (b << 16) | (g << 8) | r) >>> 0;
      };
      COLORS.forEach((name, i) => {
        palette[i] = pack(name, 255);
        palette[i + COLORS.length] = pack(name, Math.round(255 * CANVAS.dimmed));
      });
      probe.style.color = `var(${RING_COLOR})`;
      ringColor = getComputedStyle(probe).color;
      probe.remove();
    }

    function sizeCanvas() {
      dpr = window.devicePixelRatio || 1;
      canvas.width = Math.max(1, Math.round(size.width * dpr));
      canvas.height = Math.max(1, Math.round(size.height * dpr));
      ringCanvas.width = canvas.width;
      ringCanvas.height = canvas.height;
      pixels = ctx.createImageData(canvas.width, canvas.height);
      buffer = new Uint32Array(pixels.data.buffer);
    }

    // Which pixels of a w x h box belong to the ellipse inside it.
    function maskFor(w, h) {
      const key = w * 4096 + h;
      if (!masks.has(key)) {
        const mask = new Uint8Array(w * h);
        for (let y = 0; y < h; y += 1) {
          for (let x = 0; x < w; x += 1) {
            const dx = (x + 0.5) / w - 0.5;
            const dy = (y + 0.5) / h - 0.5;
            mask[y * w + x] = dx * dx + dy * dy <= 0.25 ? 1 : 0;
          }
        }
        masks.set(key, mask);
        if (masks.size > CANVAS.masks) {
          masks.delete(masks.keys().next().value);
        }
      }
      return masks.get(key);
    }

    function fill(left, top, right, bottom, color, round) {
      const width = canvas.width;
      const x0 = Math.max(0, left);
      const x1 = Math.min(width, right);
      const y0 = Math.max(0, top);
      const y1 = Math.min(canvas.height, bottom);
      if (x0 >= x1 || y0 >= y1) {
        return;
      }
      const mask = round ? maskFor(right - left, bottom - top) : null;
      for (let y = y0; y < y1; y += 1) {
        const row = y * width;
        if (x1 - x0 < 4 && !mask) {
          for (let x = row + x0; x < row + x1; x += 1) {
            buffer[x] = color;
          }
        } else if (mask) {
          const maskRow = (y - top) * (right - left) - left;
          for (let x = x0; x < x1; x += 1) {
            if (mask[maskRow + x]) {
              buffer[row + x] = color;
            }
          }
        } else {
          buffer.fill(color, row + x0, row + x1);
        }
      }
    }

    /* A small dot covers its whole cell, so neighbors tile without gaps or
       doubles. Each pixel it touches gets the color with an opacity equal to
       the share of the pixel the dot covers, blended over what is there. */
    function splat(left, top, right, bottom, slot) {
      const width = canvas.width;
      const x0 = Math.max(0, Math.floor(left));
      const x1 = Math.min(width, Math.ceil(right));
      const y0 = Math.max(0, Math.floor(top));
      const y1 = Math.min(canvas.height, Math.ceil(bottom));
      const color = palette[slot];
      const alpha = color >>> 24;
      const red = color & 255;
      const green = (color >>> 8) & 255;
      const blue = (color >>> 16) & 255;
      for (let y = y0; y < y1; y += 1) {
        const coverY = alpha * (Math.min(bottom, y + 1) - Math.max(top, y));
        const row = y * width;
        for (let x = x0; x < x1; x += 1) {
          const a = ((Math.min(right, x + 1) - Math.max(left, x)) * coverY) / 255;
          const under = buffer[row + x];
          const underA = under >>> 24;
          if (!underA || a > 0.996) {
            buffer[row + x] = ((Math.round(a * 255) << 24) | (color & 0xffffff)) >>> 0;
            continue;
          }
          const outA = a * 255 + underA * (1 - a);
          const keep = (underA * (1 - a)) / outA;
          const r = red + ((under & 255) - red) * keep;
          const g = green + (((under >>> 8) & 255) - green) * keep;
          const b = blue + (((under >>> 16) & 255) - blue) * keep;
          buffer[row + x] = ((outA << 24) | (b << 16) | (g << 8) | r) >>> 0;
        }
      }
    }

    // Draws one frame; returns true while any dot is still on its way.
    function render(now) {
      if (!buffer) {
        return false;
      }
      buffer.fill(0);
      const k = zoomNow.k * dpr;
      const shiftX = zoomNow.x * dpr;
      const shiftY = zoomNow.y * dpr;
      const travel = motion ? motion.flight : 0;
      const elapsed = motion ? now - motion.start : 0;
      const fillShare = 2 * LAYOUT.dotShare;
      let moving = false;
      for (let i = 0; i < count; i += 1) {
        if (!SHOWN[i]) {
          continue;
        }
        let x = X1[i];
        let y = Y1[i];
        if (motion) {
          const t = (elapsed - DELAY[i]) / travel;
          if (t < 1) {
            moving = true;
            const e = t <= 0 ? 0 : t * t * (3 - 2 * t);
            const dx = X1[i] - X0[i];
            const dy = Y1[i] - Y0[i];
            const curve = BEND[i] * Math.sin(Math.PI * e);
            x = X0[i] + dx * e - dy * curve;
            y = Y0[i] + dy * e + dx * curve;
          }
        }
        const cx = x * k + shiftX;
        const cy = y * k + shiftY;
        const cellW = W[i] * k;
        const cellH = H[i] * k;
        if (cellW < CANVAS.splatBelow && cellH < CANVAS.splatBelow) {
          splat(cx - cellW / 2, cy - cellH / 2, cx + cellW / 2, cy + cellH / 2, COLOR[i]);
          continue;
        }
        const halfW = (cellW * fillShare) / 2;
        const halfH = (cellH * fillShare) / 2;
        const left = Math.round(cx - halfW);
        const top = Math.round(cy - halfH);
        const right = Math.max(left + 1, Math.round(cx + halfW));
        const bottom = Math.max(top + 1, Math.round(cy + halfH));
        const round = !SQUARE[i] && right - left >= CANVAS.circleFrom;
        fill(left, top, right, bottom, palette[COLOR[i]], round);
      }
      ctx.putImageData(pixels, 0, 0);
      drawRing();
      return moving;
    }

    // The hover ring lives on its own canvas, so hovering never redraws the dots.
    function drawRing() {
      ringCtx.clearRect(0, 0, ringCanvas.width, ringCanvas.height);
      if (hovered) {
        const ring = Math.max(hovered.w, hovered.h) * LAYOUT.dotShare * zoomNow.k + HOVER.ring;
        ringCtx.beginPath();
        ringCtx.arc(zoomNow.applyX(hovered.tx) * dpr, zoomNow.applyY(hovered.ty) * dpr, ring * dpr, 0, 2 * Math.PI);
        ringCtx.lineWidth = 2 * dpr;
        ringCtx.strokeStyle = ringColor;
        ringCtx.stroke();
      }
    }

    function loop(now) {
      frame = 0;
      if (!onScreen) {
        return;
      }
      if (motion && !motion.start) {
        motion.start = now;
      }
      if (!render(now)) {
        motion = null;
      }
      if (motion) {
        frame = requestAnimationFrame(loop);
      }
    }

    function redraw() {
      if (!frame) {
        frame = requestAnimationFrame(loop);
      }
    }

    // Color slot of one dot: neutral or its rating, faded when not in focus.
    function colorOf(p) {
      const faded = p.dimmed || (current.emphasize && !current.emphasize.includes(p.rating));
      return (current.colors ? p.rating : 0) + (faded ? COLORS.length : 0);
    }

    /* New targets. Dots still travelling snap to where they were going, then
       every dot that moves leaves after a delay set by its rank, so the new
       picture fills from the center (or the bottom) out. */
    function draw(animate) {
      const flight = TRICKLE.flight;
      const spread = TRICKLE.total - flight;
      population.forEach((p, i) => {
        const was = SHOWN[i];
        SHOWN[i] = p.visible ? 1 : 0;
        if (!p.visible) {
          return;
        }
        X0[i] = !animate ? p.tx : was ? X1[i] : p.tx;
        Y0[i] = !animate ? p.ty : was ? Y1[i] : size.height + p.h;
        X1[i] = p.tx;
        Y1[i] = p.ty;
        W[i] = p.w;
        H[i] = p.h;
        COLOR[i] = colorOf(p);
        DELAY[i] = p.rank * spread;
        BEND[i] = TRICKLE.bend * (Math.random() * 2 - 1);
      });
      motion = animate ? { start: 0, flight } : null;
      redraw();
    }

    let onScreen = false;
    new IntersectionObserver(([entry]) => {
      onScreen = entry.isIntersecting;
      if (onScreen && stale) {
        relayout();
      } else if (onScreen) {
        redraw();
      }
    }, { rootMargin: NEAR_VIEWPORT }).observe(section);

    const recolor = () => {
      readColors();
      redraw();
    };
    new MutationObserver(recolor).observe(document.documentElement, { attributes: true });
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", recolor);

    // ---------------------------------------------------------- labels

    // A cluster's count and share: one line, or two on narrow screens.
    function countLines(members, twoLines) {
      if (members.length < MIN_N) {
        return [`${members.length} answered`, "(too few)"];
      }
      const lines = [fmtInt(members.length), `${Math.round(weighted(members, fairOrPoor).pct)}% fair or poor`];
      return twoLines ? lines : [lines.join(" · ")];
    }

    const shareText = (members) => (members.length < MIN_N ? "too few" : `${fpOf(members)}%`);

    function clusterLabels(clusters, view) {
      if (view.stacks) {
        return clusters.map((c) => ({
          key: c.key, name: "", count: [shareText(c.members)], x: c.mid, y: view.stacks.top, nudge: -6, dimmed: !c.focus,
        }));
      }
      const showCounts = view.counts && !(view.grid && isMobile());
      return clusters.filter((c) => c.name || showCounts).map((c) => ({
        key: c.key,
        name: c.name,
        count: showCounts ? countLines(c.members, view.grid ? view.grid.compact : isMobile()) : [],
        x: c.x,
        y: c.y - c.r,
        nudge: -6,
        dimmed: !c.focus,
      }));
    }

    // Names along the axes: years, work groups, rows, and the pizza's slices.
    function headerLabels(view) {
      const headers = [];
      if (view.columns) {
        view.columns.groups.forEach((group, i) => headers.push({
          key: `y-${group}`, text: view.columns.groupName(group),
          x: view.columns.groupX[i], y: view.columns.base + LAYOUT.yearBand / 2, anchor: "middle",
        }));
      }
      if (view.stacks) {
        const stacks = view.stacks;
        stacks.groups.forEach((group, i) => headers.push({
          key: `g-${group}`, text: shortOnMobile(group),
          x: stacks.groupX[i], y: stacks.top - LAYOUT.stackTop + LAYOUT.headerBand / 2 - 6, anchor: "middle",
        }));
        stacks.groups.forEach((group, i) => headers.push({
          key: `s-${group}`, text: stacks.subNames, small: true,
          x: stacks.groupX[i], y: stacks.base + LAYOUT.yearBand / 2, anchor: "middle",
        }));
      }
      if (view.pizza) {
        const reach = view.pizza.crust + PIZZA.labelBand * 0.6;
        const c = { x: (region().x0 + region().x1) / 2, y: (region().y0 + region().y1) / 2 };
        view.pizza.edges.forEach(({ slice, mid }) => headers.push({
          key: `p-${slice}`, text: String(slice),
          x: c.x + reach * Math.cos(mid), y: c.y + reach * Math.sin(mid), anchor: "middle",
        }));
      }
      if (view.grid) {
        const grid = view.grid;
        grid.cols.forEach((col, i) => headers.push({
          key: `c-${col}`, text: grid.compact ? SHORT_GROUP[col] || col : col,
          x: grid.colX[i], y: grid.top + LAYOUT.headerBand / 2, anchor: "middle",
        }));
        grid.rows.forEach((row, i) => headers.push({
          key: `r-${row}`, text: grid.rowName(row),
          x: grid.compact ? region().x0 : grid.left, anchor: "start",
          y: grid.compact ? grid.rowTop[i] + LAYOUT.headerBand / 2 : grid.rowY[i],
        }));
      }
      return headers;
    }

    const place = (d) => `translate(${d.px + d.dx},${d.py + d.dy})`;

    function drawLabels(clusters, view) {
      const items = clusterLabels(clusters, view);
      for (const d of items) {
        Object.assign(d, { px: zoomNow.applyX(d.x), py: zoomNow.applyY(d.y) + d.nudge, dx: 0, dy: 0 });
      }
      const groups = labels.selectAll("g.cluster-label").data(items, (d) => d.key);
      groups.exit().remove();
      const entered = groups.enter().append("g").attr("class", "cluster-label");
      entered.append("text").attr("class", "cluster-name").attr("text-anchor", "middle");
      entered.append("text").attr("class", "cluster-count").attr("text-anchor", "middle");
      const merged = entered.merge(groups).classed("is-dimmed", (d) => d.dimmed).attr("transform", place);
      merged.select(".cluster-name").attr("y", (d) => -d.count.length * TEXT.line).text((d) => d.name);
      merged.select(".cluster-count").each(function (d) {
        d3.select(this).selectAll("tspan").data(d.count).join("tspan")
          .attr("x", 0).attr("y", (line, i) => (i - d.count.length + 1) * TEXT.line).text((line) => line);
      });

      const headers = headerLabels(view);
      for (const d of headers) {
        Object.assign(d, { px: d.anchor === "start" ? d.x : zoomNow.applyX(d.x), py: zoomNow.applyY(d.y), dx: 0, dy: 0 });
      }
      const headerText = labels.selectAll("text.cluster-header").data(headers, (d) => d.key);
      headerText.exit().remove();
      headerText.enter().append("text").attr("class", "cluster-header").attr("dy", "0.35em").merge(headerText)
        .attr("text-anchor", (d) => d.anchor)
        .classed("is-small", (d) => Boolean(d.small))
        .attr("transform", place)
        .text((d) => d.text);
      separateLabels();
    }

    /* Labels never touch: each label, from the top down, moves down past any
       label already placed whose padded box it overlaps, and back inside the
       stage if it pokes out at the sides. */
    function separateLabels() {
      const nodes = labels.selectAll("g.cluster-label, text.cluster-header").nodes()
        .filter((node) => node.textContent);
      const stageBox = labels.node().getBoundingClientRect();
      const boxOf = (node) => {
        const box = node.getBoundingClientRect();
        return { left: box.left - stageBox.left, right: box.right - stageBox.left, top: box.top - stageBox.top, bottom: box.bottom - stageBox.top };
      };
      const hits = (a, b) => a.left < b.right + TEXT.pad && b.left < a.right + TEXT.pad
        && a.top < b.bottom + TEXT.pad && b.top < a.bottom + TEXT.pad;
      const placed = [];
      const ordered = nodes.map((node) => ({ node, box: boxOf(node) })).sort((a, b) => a.box.top - b.box.top);
      for (const { node, box } of ordered) {
        const d = d3.select(node).datum();
        const shiftX = Math.max(0, TEXT.pad - box.left) - Math.max(0, box.right - (size.width - TEXT.pad));
        let shiftY = 0;
        const moved = () => ({ left: box.left + shiftX, right: box.right + shiftX, top: box.top + shiftY, bottom: box.bottom + shiftY });
        for (let tries = 0; tries < placed.length; tries += 1) {
          const other = placed.find((p) => hits(moved(), p));
          if (!other) {
            break;
          }
          shiftY = other.bottom + TEXT.pad - box.top;
        }
        if (shiftX || shiftY) {
          d.dx = shiftX;
          d.dy = shiftY;
          d3.select(node).attr("transform", place);
        }
        placed.push(moved());
      }
    }

    function drawLegend(view) {
      legendBox.textContent = "";
      const items = view.colors
        ? LEGEND_ORDER.map((r) => ({ label: RATING_TEXT[r], color: `--rating-${r}` }))
        : [{ label: `Each circle is one ${PARENT[view.parent].one} who answered`, color: NEUTRAL_COLOR }];
      for (const item of items) {
        const entry = document.createElement("span");
        entry.className = "legend-item";
        const swatch = document.createElement("span");
        swatch.className = "swatch-dot";
        swatch.style.background = `var(${item.color})`;
        const text = document.createElement("span");
        text.textContent = item.label;
        entry.append(swatch, text);
        legendBox.appendChild(entry);
      }
    }

    // ---------------------------------------------------------- hover

    function personText(p) {
      const age = p.age === 0 ? "under 1" : p.age;
      return `A ${PARENT[p.parent].one} who ${WORK_TEXT[p.group].one}, with a child aged ${age}. Surveyed in ${p.year}.`;
    }

    function setHovered(p) {
      if (p !== hovered) {
        hovered = p;
        drawRing();
      }
    }

    // The dot under the pointer, or the nearest one in reach, under the zoom.
    function pointAt(event) {
      if (!finder) {
        return;
      }
      const box = canvas.getBoundingClientRect();
      const [x, y] = zoomNow.invert([event.clientX - box.left, event.clientY - box.top]);
      const found = finder.find(x, y, reach / zoomNow.k) || null;
      setHovered(found);
      if (found) {
        showTooltip(event, `Mental health: ${RATING_TEXT[found.rating]}`, personText(found));
      } else {
        hideTooltip();
      }
    }

    function clearHover() {
      setHovered(null);
      hideTooltip();
    }

    /* Mouse: the tooltip follows the pointer. Touch: a tap (little movement)
       opens it, and it stays until a tap elsewhere, a scroll or a new step. */
    let tapStart = null;
    canvas.addEventListener("pointermove", (event) => {
      if (event.pointerType !== "touch") {
        pointAt(event);
      }
    });
    canvas.addEventListener("pointerdown", (event) => {
      tapStart = event.pointerType === "touch" ? [event.clientX, event.clientY] : null;
      if (event.pointerType !== "touch") {
        pointAt(event);
      }
    });
    canvas.addEventListener("pointerup", (event) => {
      if (tapStart && Math.hypot(event.clientX - tapStart[0], event.clientY - tapStart[1]) < HOVER.tapSlop) {
        pointAt(event);
      }
      tapStart = null;
    });
    canvas.addEventListener("pointerleave", (event) => {
      if (event.pointerType !== "touch") {
        clearHover();
      }
    });
    document.addEventListener("pointerdown", (event) => {
      if (hovered && !stage.contains(event.target)) {
        clearHover();
      }
    });
    window.addEventListener("scroll", () => {
      if (hovered) {
        clearHover();
      }
    }, { passive: true });

    // ---------------------------------------------------------- zoom

    /* Zoom and pan are applied when the dots are drawn. Labels are redrawn
       at the zoomed positions, so text keeps its size. The wheel zooms only
       with Ctrl/Cmd held, so scrolling the page still scrolls the story. */
    let shown = null;
    const stageSel = d3.select(stage);

    function applyZoom(transform) {
      zoomNow = transform;
      redraw();
      stage.classList.toggle("is-zoomed", transform.k > 1);
      if (shown) {
        drawLabels(...shown);
      }
    }

    const zoom = d3.zoom()
      .scaleExtent([1, ZOOM.max])
      .filter((event) => {
        if (event.target.closest("button, .legend")) {
          return false;
        }
        if (event.type === "wheel") {
          return event.ctrlKey || event.metaKey;
        }
        if (event.type.startsWith("touch")) {
          return event.touches.length > 1 || zoomNow.k > 1;
        }
        return !event.button;
      })
      .on("start", () => stage.classList.add("is-moving"))
      .on("zoom", (event) => applyZoom(event.transform))
      .on("end", () => stage.classList.remove("is-moving"));
    stageSel.call(zoom).on("dblclick.zoom", null);

    /* Keyboard: the stage takes focus. Arrows move, + and - zoom, 0 or
       Escape fits, Enter zooms to the next group in turn. */
    let groupTurn = -1;
    stage.tabIndex = 0;
    stage.setAttribute("role", "group");
    stage.setAttribute("aria-roledescription", "interactive chart");
    stage.setAttribute("aria-label", ZOOM.keys);
    stage.addEventListener("keydown", (event) => {
      if (event.target !== stage) {
        return;
      }
      const move = ZOOM.keyStep;
      const actions = {
        ArrowLeft: () => stageSel.call(zoom.translateBy, move / zoomNow.k, 0),
        ArrowRight: () => stageSel.call(zoom.translateBy, -move / zoomNow.k, 0),
        ArrowUp: () => stageSel.call(zoom.translateBy, 0, move / zoomNow.k),
        ArrowDown: () => stageSel.call(zoom.translateBy, 0, -move / zoomNow.k),
        "+": () => glide().call(zoom.scaleBy, ZOOM.step),
        "=": () => glide().call(zoom.scaleBy, ZOOM.step),
        "-": () => glide().call(zoom.scaleBy, 1 / ZOOM.step),
        0: () => glide().call(zoom.transform, d3.zoomIdentity),
        Escape: () => glide().call(zoom.transform, d3.zoomIdentity),
        Enter: () => {
          const pieces = piecesOf(...shown);
          groupTurn = (groupTurn + 1) % pieces.length;
          zoomTo(pieces[groupTurn]);
        },
      };
      if (actions[event.key]) {
        event.preventDefault();
        actions[event.key]();
      }
    });

    const glide = () => stageSel.transition().duration(REDUCED_MOTION ? 0 : ZOOM.glide);

    function resetZoom() {
      stageSel.interrupt().call(zoom.transform, d3.zoomIdentity);
    }

    // The parts a double-click can zoom to: each pizza slice, else each cluster.
    function piecesOf(clusters, view) {
      const groups = view.pizza
        ? d3.groups(clusters[0].members, view.pizza.sliceOf).map(([, members]) => members)
        : clusters.map((c) => c.members);
      return groups.map((members) => ({
        x0: d3.min(members, (p) => p.tx), x1: d3.max(members, (p) => p.tx),
        y0: d3.min(members, (p) => p.ty), y1: d3.max(members, (p) => p.ty),
      }));
    }

    function zoomTo(piece) {
      const area = region();
      const pad = ZOOM.pad;
      const k = Math.min(ZOOM.max, Math.max(1, Math.min(
        (area.x1 - area.x0) / (piece.x1 - piece.x0 + 2 * pad),
        (area.y1 - area.y0) / (piece.y1 - piece.y0 + 2 * pad))));
      const x = (area.x0 + area.x1) / 2 - (k * (piece.x0 + piece.x1)) / 2;
      const y = (area.y0 + area.y1) / 2 - (k * (piece.y0 + piece.y1)) / 2;
      glide().call(zoom.transform, d3.zoomIdentity.translate(x, y).scale(k));
    }

    stage.addEventListener("dblclick", (event) => {
      if (event.target.closest("button")) {
        return;
      }
      const box = stage.getBoundingClientRect();
      const [x, y] = zoomNow.invert([event.clientX - box.left, event.clientY - box.top]);
      const near = (piece) => Math.hypot(
        Math.max(piece.x0 - x, 0, x - piece.x1), Math.max(piece.y0 - y, 0, y - piece.y1));
      const piece = d3.least(piecesOf(...shown), near);
      if (piece && near(piece) < ZOOM.pad) {
        zoomTo(piece);
      }
    });

    function zoomControls() {
      const box = document.createElement("div");
      box.className = "zoom-controls";
      const buttons = document.createElement("div");
      buttons.className = "zoom-buttons";
      buttons.setAttribute("role", "group");
      buttons.setAttribute("aria-label", "Zoom");
      const actions = [
        ["+", "Zoom in", () => glide().call(zoom.scaleBy, ZOOM.step)],
        ["−", "Zoom out", () => glide().call(zoom.scaleBy, 1 / ZOOM.step)],
        ["Fit", "Fit: show everything", () => glide().call(zoom.transform, d3.zoomIdentity)],
      ];
      for (const [label, name, act] of actions) {
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = label;
        button.setAttribute("aria-label", name);
        button.addEventListener("click", act);
        buttons.appendChild(button);
      }
      const hint = document.createElement("p");
      hint.className = "zoom-hint";
      hint.textContent = isMobile() ? ZOOM.hintTouch : ZOOM.hint;
      box.append(buttons, hint);
      stage.appendChild(box);
    }
    zoomControls();

    // ---------------------------------------------------------- show

    const laidOut = { width: 0, height: 0 };

    function show(view, jump, keepZoom) {
      laidOut.width = size.width;
      laidOut.height = size.height;
      const animate = Boolean(current) && !jump && !REDUCED_MOTION;
      current = view;
      clearHover();
      groupTurn = -1;
      drawLegend(view);
      measureRegion();
      const clusters = buildClusters(view);
      const spacing = fitSpacing(clusters, view);
      dot = dotSize(spacing);
      reach = Math.max(HOVER.minReach, spacing * HOVER.reach);
      setTargets(clusters, spacing, view);
      finder = d3.quadtree(population.filter((p) => p.visible), (p) => p.tx, (p) => p.ty);
      shown = [clusters, view];
      if (!keepZoom) {
        resetZoom();
      }
      drawLabels(clusters, view);
      summary.textContent = view.summary || "";
      draw(animate);
    }

    /* Re-layout only when the width changes or the height changes a lot
       (not for a phone's address bar), and only for a room on screen; the
       other catches up when it comes back. */
    let stale = false;
    function relayout() {
      stale = false;
      measure();
      if (current) {
        show(current, true, true);
      }
    }
    // The canvas always matches its box at once, so circles never stretch.
    new ResizeObserver(() => {
      if (canvas.offsetWidth !== size.width || canvas.offsetHeight !== size.height) {
        measure();
        redraw();
      }
    }).observe(canvas);

    onResize(() => {
      const phone = isMobile() && window.matchMedia("(pointer: coarse)").matches;
      const small = laidOut.width === size.width && Math.abs(size.height - laidOut.height) <= LAYOUT.resizeShare * laidOut.height;
      if (phone && small) {
        return;
      }
      if (onScreen) {
        relayout();
      } else {
        stale = true;
      }
    });

    measure();
    readColors();

    return { show };
  }

  // ================================================================ views

  const byGroup = (p) => p.group;
  const employmentGrid = (rows, rowOf, rowName) => ({ cols: EMPLOYMENT, rows, colOf: byGroup, rowOf, rowName });
  const ageGrid = () => employmentGrid(BANDS, (p) => p.band, (b) => `Child ${BAND_TEXT[b]}`);

  function exploreView(parent, choice) {
    const isParent = (p) => p.parent === parent;
    const base = { parent, colors: true, sorted: true, counts: true };
    if (!choice.group || !choice.age) {
      return { ...base, filter: isParent, grid: ageGrid(),
        summary: `Choose your work and your child's age to find the ${PARENT[parent].many} like you.` };
    }
    const age = AGE_CHOICES.find((a) => a.key === choice.age);
    const matches = (p) => p.group === choice.group && age.test(p);
    if (age.key === "baby") {
      return { ...base, filter: (p) => isParent(p) && p.age < 2, groupBy: byGroup, names: true,
        order: EMPLOYMENT, focus: matches };
    }
    return { ...base, filter: isParent, grid: ageGrid(), focus: matches };
  }

  function exploreText(parent, people, choice) {
    const names = PARENT[parent];
    const age = AGE_CHOICES.find((a) => a.key === choice.age);
    const like = people.filter((p) => p.group === choice.group && age.test(p));
    const who = `${names.many} who ${WORK_TEXT[choice.group].many} and have a child ${age.text}`;
    if (like.length < MIN_N) {
      return `Only ${like.length} ${who} answered: too few to estimate reliably.`;
    }
    const fp = weighted(like, fairOrPoor).pct;
    const high = weighted(like, highRating).pct;
    const all = weighted(people, fairOrPoor).pct;
    return `${fmtInt(like.length)} ${who} answered. About ${Math.round(fp)} in 100 rate their mental health fair or poor, and ${Math.round(high)} in 100 excellent or very good. Among all ${names.many}: ${Math.round(all)} in 100 fair or poor.`;
  }

  // Wires the "Where would you stand?" buttons and adds the step's view.
  function setUpExplore(room, sectionId, parent, people, steps) {
    const box = document.querySelector(`#${sectionId} .step-explore`);
    const result = box.querySelector(".explore-result");
    const choice = { group: null, age: null };
    const options = {
      group: EMPLOYMENT.map((g) => [g, g]),
      age: AGE_CHOICES.map((a) => [a.key, a.label]),
    };
    for (const container of box.querySelectorAll(".controls")) {
      const key = container.dataset.choice;
      for (const [value, label] of options[key]) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "pill";
        button.textContent = label;
        button.setAttribute("aria-pressed", "false");
        button.addEventListener("click", () => {
          choice[key] = value;
          for (const other of container.querySelectorAll("button")) {
            other.setAttribute("aria-pressed", String(other === button));
          }
          if (choice.group && choice.age) {
            box.classList.add("has-choice");
            const text = exploreText(parent, people, choice);
            result.textContent = text;
            room.show({ ...exploreView(parent, choice), summary: text });
          }
        });
        container.appendChild(button);
      }
    }
    const previous = steps[steps.length - 1];
    steps.push(() => (choice.group && choice.age ? exploreView(parent, choice) : previous()));
  }

  // ---- Mothers
  const motherRoom = createRoom("room", mothers);
  const sortedMothers = { parent: "mothers", colors: true, sorted: true, counts: true };
  const motherGroups = { ...sortedMothers, groupBy: byGroup, names: true, order: EMPLOYMENT };
  const motherSteps = [
    () => ({ parent: "mothers", summary: `${STATS.mothersCount} circles, one for each mother who answered.` }),
    () => ({ parent: "mothers", colors: true,
      sorted: true, pizza: { slices: YEARS, sliceOf: (p) => p.year },
      summary: `The circles take the color of each mother's mental health rating, in one pie: a slice per survey year, a ring per answer from excellent in the middle to poor at the crust; ${STATS.mothersFp} in 100 say fair or poor.` }),
    () => ({ parent: "mothers", colors: true,
      columns: {
        groups: YEARS, groupOf: (p) => p.year, groupName: (year) => String(year),
        subs: [1, 2, 3, 4, 5], subOf: (p) => p.rating,
      },
      summary: "The circles line up in columns by survey year and rating, from excellent to poor." }),
    () => ({ ...motherGroups,
      summary: "The mothers sort into four groups by work, with excellent ratings in the center of each and poor at the rim." }),
    () => ({ ...motherGroups, focus: (p) => p.group === "Looking for work",
      summary: `Mothers looking for work are highlighted: ${STATS.lookingFp} in 100 say fair or poor.` }),
    () => ({ ...motherGroups, emphasize: [1, 2],
      summary: `Only excellent or very good ratings are shown in full: ${STATS.fullTimeHigh} in 100 full-time mothers, ${STATS.lookingHigh} in 100 mothers looking for work.` }),
    () => ({ ...sortedMothers, grid: ageGrid(), focus: (p) => p.group === "Not looking for work",
      summary: `Each group is split by the child's age; mothers not looking for work with a teenager: ${STATS.notLookingTeenFp} in 100.` }),
    () => ({ ...motherGroups, filter: (p) => p.age < 2, focus: (p) => p.group === "Full-time",
      summary: `Only mothers of children under 2; full-time mothers are highlighted: ${STATS.babyFullTimeFp} in 100 say fair or poor.` }),
  ];
  setUpExplore(motherRoom, "room", "mothers", mothers, motherSteps);
  // A segmented switcher jumps straight to a view; scrolling keeps it in sync.
  function viewSwitch(sectionId, room, steps, choices) {
    const box = document.querySelector(`#${sectionId} .view-switch`);
    const buttons = choices.map(([label, step]) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = label;
      button.dataset.step = step;
      button.addEventListener("click", () => select(step));
      box.appendChild(button);
      return button;
    });
    function mark(step) {
      // The last choice at or before this step stays pressed.
      let active = null;
      for (const button of buttons) {
        if (Number(button.dataset.step) <= step) {
          active = button;
        }
      }
      buttons.forEach((b) => b.setAttribute("aria-pressed", String(b === active)));
    }
    function select(step) {
      room.show(steps[step]());
      mark(step);
    }
    return select;
  }

  const showMotherStep = viewSwitch("room", motherRoom, motherSteps,
    [["Crowd", 0], ["Pizza", 1], ["Years", 2], ["Work", 3], ["Child's age", 6], ["Under 2", 7]]);
  onSteps("room", showMotherStep);

  // ---- Fathers, with mothers alongside for comparison
  const parentRoom = createRoom("dads-room", mothers.concat(fathers));
  const bothParents = { parent: "fathers", colors: true, sorted: true,
    stacks: { groups: EMPLOYMENT, groupOf: byGroup, subs: ["mothers", "fathers"], subOf: (p) => p.parent, subNames: "M · F" } };
  const fatherSteps = [
    () => ({ parent: "fathers", filter: (p) => p.parent === "fathers", colors: true,
      summary: `${STATS.fathersCount} circles, one for each father who answered; ${STATS.fathersFp} in 100 say fair or poor.` }),
    () => ({ ...bothParents,
      summary: "Mothers and fathers side by side in 100% stacked columns for each work group, excellent at the bottom and poor at the top, with the weighted share fair or poor above each column." }),
    () => ({ ...bothParents, focus: (p) => p.group !== "Full-time",
      summary: `Parents out of work are highlighted; fathers looking for work: ${STATS.fathersLookingFp} in 100 say fair or poor.` }),
  ];
  setUpExplore(parentRoom, "dads-room", "fathers", fathers, fatherSteps);
  const showFatherStep = viewSwitch("dads-room", parentRoom, fatherSteps, [["Fathers", 0], ["Side by side", 1]]);
  onSteps("dads-room", showFatherStep);

  // ================================================================ table

  const tableRows = [];
  for (const [parent, people] of [["mothers", mothers], ["fathers", fathers]]) {
    for (const group of EMPLOYMENT) {
      for (const age of AGE_CHOICES) {
        const like = people.filter((p) => p.group === group && age.test(p));
        const tooFew = like.length < MIN_N;
        tableRows.push({
          parent: PARENT[parent].title, group, age: age.label, n: fmtInt(like.length),
          fp: tooFew ? "too few" : weighted(like, fairOrPoor).pct.toFixed(1),
          high: tooFew ? "too few" : weighted(like, highRating).pct.toFixed(1),
        });
      }
    }
  }
  table("room-table",
    [{ label: "Parent", value: (r) => r.parent }, { label: "Work", value: (r) => r.group },
      { label: "Child's age", value: (r) => r.age }, { label: "Respondents", value: (r) => r.n },
      { label: "Fair or poor (%)", value: (r) => r.fp }, { label: "Excellent or very good (%)", value: (r) => r.high }],
    tableRows);

  initThemeToggle("theme-toggle");
})();
