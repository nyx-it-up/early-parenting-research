/* Statistics 101: each method in the study explained as a short, step-by-step
   animated build (in the spirit of 3Blue1Brown). Drawn into [data-stats101].
   Scenes tagged "Illustration" use made-up numbers to show how a method works;
   "Study results" scenes use the study's estimates (data.js).
   Each scene is a list of beats. Going to beat k redraws beats 0..k-1 instantly
   and animates beat k, so Back, Next and Play always land on the same picture.
   Every scene can be zoomed (wheel, pinch, buttons) and dragged. */

(function () {
  "use strict";

  // ================================================================ settings

  const DATA = window.STORY_DATA;
  const REDUCED = window.Viz.REDUCED_MOTION;
  const W = 560;
  const H = 260;
  const PAUSE = 2600; // reading time between beats when playing
  const SPEED = { short: 500, long: 1100 };
  const LABEL_GAP = 22; // minimum distance between stacked labels, in drawing units
  const ZOOM = { min: 1, max: 6, step: 1.6 };
  const COLOR = { a: "var(--series-1)", b: "var(--accent)", muted: "var(--muted)", ink: "var(--ink)" };
  const fmt1 = d3.format(".1f");
  const pct = (v) => `${Math.round(v * 100)}%`;

  // ================================================================ helpers

  // Animate when d > 0; otherwise set the end state at once.
  function tr(selection, d, duration = SPEED.long, delay = 0) {
    return d ? selection.transition().duration(duration * d).delay(delay * d).ease(d3.easeCubicInOut) : selection;
  }

  // Run fn(t) from 0 to 1 over time, or once at t = 1.
  function tween(owner, d, duration, fn) {
    if (!d) {
      fn(1);
      return;
    }
    owner.transition("morph").duration(duration * d).ease(d3.easeCubicInOut).tween("morph", () => fn);
  }

  function label(svg, x, y, value, cls = "s101-label", anchor = "start") {
    return svg.append("text").attr("class", cls).attr("x", x).attr("y", y).attr("text-anchor", anchor).text(value);
  }

  function axisBottom(svg, scale, y, format, ticks = 5) {
    return svg.append("g").attr("class", "s101-axis").attr("transform", `translate(0,${y})`)
      .call(d3.axisBottom(scale).ticks(ticks).tickFormat(format));
  }

  // An equation built from coloured pieces, [[text, colour], ...], hidden until shown.
  function equation(svg, x, y, parts, anchor = "start") {
    const t = svg.append("text").attr("class", "s101-eq").attr("x", x).attr("y", y).attr("text-anchor", anchor).attr("opacity", 0);
    parts.forEach(([text, color]) => t.append("tspan").attr("fill", color || COLOR.ink).text(text));
    return t;
  }

  // Chart titles live in HTML above the drawing, so long ones wrap on phones.
  let setHeading = () => {};

  const show = (selection, d, delay = 0) => tr(selection, d, SPEED.short, delay).attr("opacity", 1);
  const hide = (selection, d) => tr(selection, d, SPEED.short).attr("opacity", 0);

  // A horizontal bar on a 0..max scale with a value label that counts up.
  function makeBar(svg, { x, y, width, max, color, title, suffix = "%" }) {
    svg.append("rect").attr("class", "s101-track").attr("x", x).attr("y", y).attr("width", width).attr("height", 18);
    const fill = svg.append("rect").attr("x", x).attr("y", y).attr("height", 18).attr("width", 0).attr("fill", color);
    const value = label(svg, x + 6, y + 13, "", "s101-value");
    const caption = label(svg, x, y - 10, title);
    let current = 0;
    return {
      caption,
      to(v, d) {
        const from = current;
        current = v;
        tr(fill, d).attr("width", (width * v) / max);
        tr(value, d).attr("x", x + (width * v) / max + 6);
        tween(value, d, SPEED.long, (t) => value.text(`${fmt1(from + (v - from) * t)}${suffix}`));
      },
    };
  }

  // ================================================================ scenes

  const SCENES = {};

  // ---------------------------------------------------------------- weights
  SCENES.weights = {
    illustration: true,
    setup(svg) {
      const people = d3.range(10).map((i) => ({ group: i < 6 ? "a" : "b", weight: i < 6 ? 1 : 3 }));
      const dots = svg.selectAll("circle.p").data(people).enter().append("circle")
        .attr("class", "p").attr("cx", (p, i) => 50 + i * 48).attr("cy", 80).attr("r", 10)
        .attr("fill", (p) => COLOR[p.group]).attr("opacity", 0);
      const weights = svg.selectAll("text.w").data(people).enter().append("text")
        .attr("class", "s101-note w").attr("text-anchor", "middle")
        .attr("x", (p, i) => 50 + i * 48).attr("y", 130).text((p) => `×${p.weight}`).attr("opacity", 0);
      const bar = makeBar(svg, { x: 50, y: 180, width: 440, max: 100, color: COLOR.b, title: "Orange share, counting answers" });
      const eq = equation(svg, 50, 245, [["share = ", null], ["Σ weight × orange", COLOR.b], [" ÷ ", null], ["Σ weight", COLOR.a]]);
      return { dots, weights, bar, eq };
    },
    beats: [
      { say: "Ten people answered. Six come from a group the survey reaches easily (blue), four from a group it reaches less often (orange).",
        run: (c, d) => c.dots.each(function (p, i) { show(d3.select(this), d, i * 60); }) },
      { say: "Count answers and orange is 4 of 10: 40%. But orange families were under-sampled, so 40% understates them.",
        run: (c, d) => c.bar.to(40, d) },
      { say: "A weight says how many families each answer stands for. Each orange answer stands for 3, each blue for 1.",
        run: (c, d) => {
          show(c.weights, d);
          tr(c.dots, d).attr("r", (p) => 10 * Math.sqrt(p.weight));
        } },
      { say: "Count weight instead of heads: 4 × 3 = 12 out of 6 + 12 = 18. The weighted share is 66.7%, the share in the population.",
        run: (c, d) => {
          c.bar.caption.text("Orange share, counting weights");
          c.bar.to(66.7, d);
          show(c.eq, d);
        } },
    ],
  };

  // ---------------------------------------------------------------- uncertainty
  SCENES.uncertainty = {
    illustration: true,
    setup(svg) {
      const x = d3.scaleLinear().domain([4, 12]).range([40, 520]);
      const step = 7;
      axisBottom(svg, x, 210, (v) => `${v}%`, 8);
      const random = d3.randomNormal.source(d3.randomLcg(7))(8, 1);
      const counts = {};
      const samples = d3.range(80).map(() => {
        const key = Math.round(Math.max(4.25, Math.min(11.75, random())) * 4) / 4;
        counts[key] = (counts[key] || 0) + 1;
        return { key, stack: counts[key] };
      });
      const dots = svg.selectAll("circle").data(samples).enter().append("circle")
        .attr("cx", (s) => x(s.key)).attr("cy", 30).attr("r", 3.5).attr("fill", COLOR.a).attr("opacity", 0);
      // Expected pile height for 80 draws in 0.25-wide bins.
      const curve = svg.append("path").attr("class", "s101-curve").attr("stroke", COLOR.b).attr("opacity", 0)
        .attr("d", d3.line()(d3.range(4, 12.01, 0.1).map((v) => [x(v), 206 - step * 80 * 0.25 * Math.exp(-((v - 8) ** 2) / 2) / Math.sqrt(2 * Math.PI)])));
      const lo = x(8 - 1.96);
      const hi = x(8 + 1.96);
      const bracket = svg.append("path").attr("class", "s101-bracket").attr("d", `M${lo},72V62H${hi}V72`).attr("opacity", 0);
      const eq = equation(svg, 280, 52, [["estimate ", null], ["± 1.96 × standard error", COLOR.b]], "middle");
      return { dots, curve, bracket, eq, cy: (s) => 206 - s.stack * step };
    },
    beats: [
      { say: "One survey gives one estimate: say 8% of mothers report fair or poor mental health.",
        run: (c, d) => tr(c.dots.filter((s, i) => i === 0), d).attr("opacity", 1).attr("cy", c.cy) },
      { say: "Had different households been picked, the answer would land elsewhere. Imagine running the survey again and again.",
        run: (c, d) => c.dots.filter((s, i) => i > 0).each(function (s, i) {
          tr(d3.select(this), d, SPEED.short, i * 35).attr("opacity", 1).attr("cy", c.cy(s));
        }) },
      { say: "The estimates pile into a bell shape around the truth. Its spread is the standard error.",
        run: (c, d) => show(c.curve, d) },
      { say: "About 95% of them fall within 1.96 standard errors: the 95% confidence interval. The study's errors also follow how NSCH picked households, by state and stratum.",
        run: (c, d) => { show(c.bracket, d); show(c.eq, d); } },
    ],
  };

  // ---------------------------------------------------------------- logistic regression
  const LOGIT = { a: 1.5, b: -0.6, shift: Math.log(1.48) };
  const prob = (z) => 1 / (1 + Math.exp(-z));
  const logOdds = (p) => Math.log(p / (1 - p));
  SCENES.logistic = {
    illustration: true,
    setup(svg) {
      const x = d3.scaleLinear().domain([0, 10]).range([60, 520]);
      const yP = d3.scaleLinear().domain([0, 1]).range([210, 40]);
      const yL = d3.scaleLinear().domain([-5, 3]).range([210, 40]);
      const random = d3.randomLcg(5);
      const mothers = d3.range(140).map(() => {
        const income = random() * 10;
        return { income, y: random() < prob(LOGIT.a + LOGIT.b * income) ? 1 : 0, jitter: (random() - 0.5) * 10 };
      });
      const bins = d3.range(5).map((k) => {
        const inBin = mothers.filter((m) => m.income >= k * 2 && m.income < k * 2 + 2);
        return { mid: k * 2 + 1, share: Math.min(0.97, Math.max(0.03, d3.mean(inBin, (m) => m.y))) };
      });
      // Least-squares straight line through the bin shares.
      const mx = d3.mean(bins, (b) => b.mid);
      const my = d3.mean(bins, (b) => b.share);
      const slope = d3.sum(bins, (b) => (b.mid - mx) * (b.share - my)) / d3.sum(bins, (b) => (b.mid - mx) ** 2);
      const lineAt = (v) => my + slope * (v - mx);

      const state = { t: 0 }; // 0 = probability scale, 1 = log-odds scale
      const yOf = (p) => (1 - state.t) * yP(p) + state.t * yL(logOdds(p));

      axisBottom(svg, x, 218, (v) => (v === 0 ? "low" : v === 10 ? "high" : ""), 2);
      label(svg, 290, 250, "family income →", "s101-note", "middle");
      const yAxis = svg.append("g").attr("class", "s101-axis");
      const yTitle = label(svg, 14, 26, "", "s101-note");

      const dots = svg.selectAll("circle.m").data(mothers).enter().append("circle").attr("class", "m")
        .attr("cx", (m) => x(m.income)).attr("cy", (m) => yP(m.y) + m.jitter).attr("r", 3.2)
        .attr("fill", (m) => (m.y ? COLOR.b : COLOR.a)).attr("opacity", 0);
      const binDots = svg.selectAll("circle.bin").data(bins).enter().append("circle").attr("class", "bin")
        .attr("cx", (b) => x(b.mid)).attr("r", 7).attr("fill", COLOR.ink).attr("opacity", 0);
      const straight = svg.append("path").attr("class", "s101-wrong").attr("opacity", 0)
        .attr("d", `M${x(-0.5)},${yP(lineAt(-0.5))}L${x(10.5)},${yP(lineAt(10.5))}`);
      const wrongNote = label(svg, x(10.2), yP(lineAt(10.5)) - 4, "below 0%?", "s101-note", "end").attr("opacity", 0);

      const samples = d3.range(0, 10.01, 0.1);
      const curves = [0, LOGIT.shift].map((shift, i) => svg.append("path").attr("class", "s101-curve")
        .attr("stroke", i ? COLOR.b : COLOR.ink).attr("opacity", 0).datum(shift));
      const eq = equation(svg, 380, 62, [["log-odds", COLOR.ink], [" = ", null], ["a", COLOR.a], [" + ", null], ["b", COLOR.b], [" × income", null]], "middle");
      const eq2 = equation(svg, 380, 62, [["odds ratio = e", null], ["shift", COLOR.b], [" = 1.48", COLOR.b]], "middle");
      const groupNote = label(svg, x(10), 0, "looking for work", "s101-note", "end").attr("opacity", 0).attr("fill", COLOR.b);

      function redraw() {
        const onLogit = state.t >= 0.5;
        const ticks = onLogit ? [0.01, 0.05, 0.2, 0.5, 0.8, 0.95] : [0, 0.25, 0.5, 0.75, 1];
        yAxis.selectAll("*").remove();
        ticks.forEach((p) => {
          const safe = Math.min(0.995, Math.max(0.005, p));
          yAxis.append("text").attr("x", 52).attr("y", yOf(safe) + 4).attr("text-anchor", "end")
            .text(onLogit ? fmt1(logOdds(p)) : pct(p));
        });
        yTitle.text(onLogit ? "log-odds of fair or poor" : "chance of fair or poor");
        binDots.attr("cy", (b) => yOf(b.share));
        curves.forEach((path) => path.attr("d", d3.line()(samples.map((v) => [x(v), yOf(prob(LOGIT.a + LOGIT.b * v + path.datum()))]))));
        groupNote.attr("y", yOf(prob(LOGIT.a + LOGIT.b * 10 + LOGIT.shift)) - 8);
      }
      redraw();
      const morph = (to, d) => {
        const from = state.t;
        tween(yAxis, d, SPEED.long * 1.6, (t) => { state.t = from + (to - from) * t; redraw(); });
      };
      return { dots, binDots, straight, wrongNote, curves, eq, eq2, groupNote, morph };
    },
    beats: [
      { say: "Each dot is a mother. Her answer is 1 (fair or poor, orange, top) or 0 (blue, bottom). Income runs left to right.",
        run: (c, d) => c.dots.each(function (m, i) { show(d3.select(this), d, i * 6); }) },
      { say: "Average each income slice: the share answering 1 falls as income rises. That share is what we want to model.",
        run: (c, d) => { show(c.binDots, d); tr(c.dots, d).attr("opacity", 0.25); } },
      { say: "A straight line can't do it: carried far enough, it predicts shares below 0% or above 100%.",
        run: (c, d) => { show(c.straight, d); show(c.wrongNote, d); } },
      { say: "So change the scale. Odds = p ÷ (1 − p), and the log of the odds stretches 0–100% out to run from −∞ to +∞. Watch the axis stretch.",
        run: (c, d) => {
          hide(c.straight, d);
          hide(c.wrongNote, d);
          hide(c.dots, d);
          c.morph(1, d);
        } },
      { say: "On the log-odds scale the points fall along a straight line. Logistic regression fits that line: log-odds = a + b × income.",
        run: (c, d) => { show(c.curves[0], d); show(c.eq, d); } },
      { say: "Now squeeze the axis back to percentages. The straight line bends into an S-curve that can never leave 0–100%.",
        run: (c, d) => { hide(c.eq, d); c.morph(0, d); } },
      { say: "Add employment: mothers looking for work get the same curve, shifted up by one fixed amount on the log-odds scale. e to that shift is the odds ratio: 1.48 in the study's main model.",
        run: (c, d) => { show(c.curves[1], d); show(c.groupNote, d); show(c.eq2, d); } },
    ],
  };

  // ---------------------------------------------------------------- adjusted models (study results)
  SCENES.models = {
    setup(svg) {
      const gaps = Object.fromEntries(DATA.adjustedGaps.filter((g) => g.group === "Looking for work").map((g) => [g.model, g.gap]));
      setHeading("Gap: mothers looking for work vs. full-time (percentage points)");
      const bar = makeBar(svg, { x: 40, y: 130, width: 440, max: 8, color: COLOR.b, title: "", suffix: " pts" });
      return { gaps, bar };
    },
    beats: [
      { say: "M0, the raw comparison: only the child's age and survey year are held equal.",
        run: (c, d) => { c.bar.caption.text("M0: child's age and year"); c.bar.to(c.gaps.M0, d); } },
      { say: "M1, the main model, compares mothers with the same income, education, marital status, number of children and age. The gap shrinks: part of it came from those differences.",
        run: (c, d) => { c.bar.caption.text("M1: + income, education, family, age"); c.bar.to(c.gaps.M1, d); } },
      { say: "M2 also holds physical health equal, as a check. A gap remains, but holding things equal never proves cause: something unmeasured could still explain it.",
        run: (c, d) => { c.bar.caption.text("M2: + physical health"); c.bar.to(c.gaps.M2, d); } },
    ],
  };

  // ---------------------------------------------------------------- predictive margins
  SCENES.margins = {
    illustration: true,
    setup(svg) {
      const random = d3.randomLcg(3);
      const mothers = d3.range(14).map(() => ({ base: 0.04 + random() * 0.08 }));
      const height = (m, k) => m.base * k * 900;
      const mean = (k) => 200 - d3.mean(mothers, (m) => height(m, k));
      const bars = svg.selectAll("rect.m").data(mothers).enter().append("rect").attr("class", "m")
        .attr("x", (m, i) => 40 + i * 34).attr("width", 22).attr("fill", COLOR.a).attr("y", 200).attr("height", 0);
      const tag = label(svg, 40, 228, "", "s101-value");
      const lines = [1, 1.45].map((k, i) => svg.append("line").attr("class", "s101-mean").attr("x1", 36).attr("x2", 520)
        .attr("y1", mean(k)).attr("y2", mean(k)).attr("stroke", i ? COLOR.b : COLOR.a).attr("opacity", 0));
      const gap = svg.append("path").attr("class", "s101-bracket").attr("opacity", 0).attr("d", `M524,${mean(1)}H530V${mean(1.45)}H524`);
      const gapLabel = label(svg, 520, mean(1.45) - 8, "gap", "s101-value", "end").attr("opacity", 0);
      return { bars, height, tag, lines, gap, gapLabel };
    },
    beats: [
      { say: "Each bar is one mother's predicted chance of fair or poor mental health, from her own income, age and family.",
        run: (c, d) => { c.tag.text("Everyone set to: full-time"); tr(c.bars, d).attr("y", (m) => 200 - c.height(m, 1)).attr("height", (m) => c.height(m, 1)); } },
      { say: "Average the predictions: that's the adjusted percentage for full-time.",
        run: (c, d) => show(c.lines[0], d) },
      { say: "Now relabel every one of them as looking for work, change nothing else, and predict again.",
        run: (c, d) => {
          c.tag.text("Everyone set to: looking for work");
          tr(c.bars, d).attr("fill", COLOR.b).attr("y", (m) => 200 - c.height(m, 1.45)).attr("height", (m) => c.height(m, 1.45));
        } },
      { say: "The new average minus the old one is the adjusted gap. Same mothers; only the job label moved.",
        run: (c, d) => { show(c.lines[1], d); show(c.gap, d); show(c.gapLabel, d); } },
    ],
  };

  // ---------------------------------------------------------------- imputations
  SCENES.imputations = {
    illustration: true,
    setup(svg) {
      const x = d3.scaleLinear().domain([0, 400]).range([40, 520]);
      axisBottom(svg, x, 170, (v) => `${v}%`);
      label(svg, 280, 205, "family income, % of poverty line", "s101-note", "middle");
      const guesses = [150, 190, 170, 230, 160, 210];
      const dots = svg.selectAll("circle").data(guesses).enter().append("circle")
        .attr("cx", 280).attr("cy", 40).attr("r", 7).attr("fill", COLOR.b).attr("opacity", 0);
      const unknown = label(svg, 280, 46, "?", "s101-eq", "middle");
      const band = svg.append("rect").attr("class", "s101-band").attr("x", x(150)).attr("y", 70).attr("height", 90).attr("width", 0);
      const eq = equation(svg, 280, 240, [["uncertainty = ", null], ["within", COLOR.a], [" + ", null], ["between", COLOR.b]], "middle");
      return { x, dots, unknown, band, eq };
    },
    beats: [
      { say: "One family left its income blank.", run: () => {} },
      { say: "The Census Bureau fills it in six times, each a plausible value drawn from similar families.",
        run: (c, d) => {
          hide(c.unknown, d);
          c.dots.each(function (g, i) { tr(d3.select(this), d, SPEED.long, i * 180).attr("opacity", 0.9).attr("cx", c.x(g)).attr("cy", 150 - i * 13); });
        } },
      { say: "Every model runs on all six versions. How much the six disagree is uncertainty about income itself.",
        run: (c, d) => tr(c.band, d).attr("width", c.x(230) - c.x(150)) },
      { say: "Rubin's rules average the six results and add that disagreement to the usual uncertainty, so intervals stay honest.",
        run: (c, d) => show(c.eq, d) },
    ],
  };

  // ---------------------------------------------------------------- age interaction (study results)
  SCENES.interaction = {
    setup(svg) {
      const bands = ["0-5", "6-11", "12-17"];
      const x = d3.scalePoint().domain(bands).range([70, 380]);
      const y = d3.scaleLinear().domain([-1, 7]).range([200, 50]);
      axisBottom(svg, x, 205, (b) => `child ${b}`);
      setHeading("Adjusted gap vs. full-time mothers (percentage points)");
      const series = [["Looking for work", COLOR.a], ["Not looking for work", COLOR.b]].map(([group, color]) => {
        const rows = bands.map((band) => DATA.gapsByBand.find((r) => r.group === group && r.band === band));
        const path = svg.append("path").attr("class", "s101-curve").attr("stroke", color).attr("opacity", 0);
        const name = label(svg, 390, 0, group.replace(" for work", ""), "s101-note").attr("fill", color).attr("opacity", 0);
        return { rows, average: d3.mean(rows, (r) => r.gap), path, name };
      });
      const state = { t: 0 };
      function redraw() {
        series.forEach((s) => {
          const points = s.rows.map((r) => [x(r.band), y(s.average + (r.gap - s.average) * state.t)]);
          s.path.attr("d", d3.line()(points));
          s.labelY = points[2][1] + 4;
        });
        const [a, b] = series;
        const gap = LABEL_GAP - Math.abs(a.labelY - b.labelY);
        if (gap > 0) {
          const up = a.labelY <= b.labelY ? a : b;
          up.labelY -= gap / 2;
          (up === a ? b : a).labelY += gap / 2;
        }
        series.forEach((s) => s.name.attr("y", s.labelY));
      }
      redraw();
      const owner = series[0].path;
      return { series, bend: (d) => tween(owner, d, SPEED.long * 1.6, (t) => { state.t = t; redraw(); }) };
    },
    beats: [
      { say: "A model without an interaction allows one gap per group, the same at every child's age: flat lines.",
        run: (c, d) => c.series.forEach((s) => { show(s.path, d); show(s.name, d); }) },
      { say: "Let the gap differ by the child's age, and the lines bend to the study's estimates.",
        run: (c, d) => c.bend(d) },
      { say: "Is the bending more than noise? A Wald test compares the two models: χ²(6) = 20.2, p = .003. The gaps do change with the child's age.",
        run: () => {} },
    ],
  };

  // ---------------------------------------------------------------- reliability
  SCENES.reliability = {
    illustration: true,
    setup(svg, extra) {
      const x = d3.scaleLinear().domain([0, 20]).range([40, 520]);
      axisBottom(svg, x, 170, (v) => `${v}%`);
      const band = svg.append("rect").attr("class", "s101-band").attr("y", 100).attr("height", 30);
      const dot = svg.append("circle").attr("cx", x(10)).attr("cy", 115).attr("r", 7).attr("fill", COLOR.b);
      const verdict = label(svg, 280, 80, "", "s101-value", "middle");
      equation(svg, 280, 225, [["interval width ∝ ", null], ["1 ÷ √n", COLOR.b]], "middle").attr("opacity", 1);
      const slider = document.createElement("input");
      Object.assign(slider, { type: "range", min: 10, max: 2000, value: 200, className: "s101-slider" });
      slider.setAttribute("aria-label", "Number of respondents");
      extra.appendChild(slider);
      function update(n, d = 0) {
        slider.value = n;
        const half = 1.96 * Math.sqrt((0.1 * 0.9) / n) * 100;
        const lo = x(Math.max(0, 10 - half));
        tr(band, d).attr("x", lo).attr("width", x(Math.min(20, 10 + half)) - lo);
        const tooFew = n < 30;
        dot.attr("opacity", tooFew ? 0.25 : 1);
        band.attr("opacity", tooFew ? 0.25 : 1);
        verdict.text(tooFew ? `${n} people: too few, not reported` : `${n} people: 10% ± ${fmt1(half)} points`);
      }
      slider.addEventListener("input", () => update(Number(slider.value)));
      return { update };
    },
    beats: [
      { say: "With 2,000 answers, a 10% estimate is pinned down tightly.", run: (c, d) => c.update(2000, d) },
      { say: "With 200, the interval is about three times wider: it shrinks only with the square root of the sample size.", run: (c, d) => c.update(200, d) },
      { say: "Below 30 answers, NSCH advises not reporting the estimate at all. Drag the slider to try it.", run: (c, d) => c.update(20, d) },
    ],
  };

  // ---------------------------------------------------------------- under 2
  SCENES.under2 = {
    illustration: true,
    setup(svg) {
      const random = d3.randomLcg(11);
      const people = d3.range(90).map((i) => ({ i, baby: random() < 0.11 }));
      const babies = people.filter((p) => p.baby);
      const dots = svg.selectAll("circle").data(people).enter().append("circle")
        .attr("cx", (p) => 40 + (p.i % 18) * 18).attr("cy", (p) => 70 + Math.floor(p.i / 18) * 18).attr("r", 6)
        .attr("fill", COLOR.muted);
      const note = label(svg, 380, 60, "On their own", "s101-note").attr("opacity", 0);
      return { dots, babies, note };
    },
    beats: [
      { say: "All mothers in the study.", run: () => {} },
      { say: "About 1 in 9 has a child under 2.", run: (c, d) => tr(c.dots.filter((p) => p.baby), d).attr("fill", COLOR.b) },
      { say: "They're analyzed on their own, to test whether full-time work is harder with a baby. The study found no sign of it, though the group is small.",
        run: (c, d) => {
          tr(c.dots.filter((p) => !p.baby), d).attr("opacity", 0.15);
          tr(c.dots.filter((p) => p.baby), d)
            .attr("cx", (p) => 380 + (c.babies.indexOf(p) % 5) * 22).attr("cy", (p) => 80 + Math.floor(c.babies.indexOf(p) / 5) * 22);
          show(c.note, d);
        } },
    ],
  };

  // ---------------------------------------------------------------- both ends (study results)
  function growRow(c, row, d) {
    tr(row.left, d).attr("x", c.mid - row.high * c.k).attr("width", row.high * c.k);
    tr(row.right, d).attr("width", row.low * c.k);
    row.tags.forEach((t) => show(t, d));
  }
  SCENES.bothEnds = {
    setup(svg) {
      const mid = 300;
      const k = 3.1;
      label(svg, mid - 10, 40, "← excellent or very good", "s101-note", "end");
      label(svg, mid + 10, 40, "fair or poor →", "s101-note");
      const rows = [["Full-time", 66.2, 7.3, 80], ["Looking for work", 60.8, 10.3, 150]].map(([name, high, low, y]) => {
        label(svg, mid, y - 8, name, "s101-label", "middle");
        const left = svg.append("rect").attr("x", mid).attr("y", y).attr("height", 22).attr("width", 0).attr("fill", COLOR.a);
        const right = svg.append("rect").attr("x", mid).attr("y", y).attr("height", 22).attr("width", 0).attr("fill", COLOR.b);
        const tags = [
          label(svg, mid - high * k - 6, y + 16, `${high}%`, "s101-value", "end"),
          label(svg, mid + low * k + 6, y + 16, `${low}%`, "s101-value"),
        ];
        tags.forEach((t) => t.attr("opacity", 0));
        return { high, low, left, right, tags };
      });
      return { rows, mid, k };
    },
    beats: [
      { say: "The main study looks at the bottom of the scale, fair or poor. Here are full-time mothers at both ends (adjusted %).",
        run: (c, d) => growRow(c, c.rows[0], d) },
      { say: "Mothers looking for work: fewer at the top (−5.4 points) and more at the bottom. They're behind at both ends.",
        run: (c, d) => growRow(c, c.rows[1], d) },
    ],
  };

  // ---------------------------------------------------------------- decomposition (study results)
  SCENES.decomposition = {
    setup(svg) {
      const result = DATA.decomposition.find((r) => r.group === "Looking for work");
      const parts = result.contributions.filter((p) => p.pts > 0.1).sort((a, b) => b.pts - a.pts);
      const x = d3.scaleLinear().domain([0, result.raw]).range([40, 500]);
      let start = 0;
      const rows = parts.map((p) => ({ name: p.name, from: start, to: (start += p.pts), color: COLOR.b }))
        .concat([{ name: "Not explained", from: start, to: result.raw, color: COLOR.muted }])
        .map((r, i) => {
          const y = 50 + i * 32;
          const text = label(svg, x(r.from), y - 4, `${r.name} +${fmt1(r.to - r.from)}`, "s101-note").attr("opacity", 0);
          const rect = svg.append("rect").attr("x", x(r.from)).attr("y", y).attr("height", 16).attr("width", 0).attr("fill", r.color);
          return { text, rect, width: x(r.to) - x(r.from) };
        });
      return { rows };
    },
    beats: [
      { say: "The raw gap between mothers looking for work and full-time mothers is 6.7 points. How much do measured differences account for?",
        run: () => {} },
      { say: "Give mothers looking for work the full-time mothers' mix of marital status, age, income and education, one factor at a time, and see how much the gap closes.",
        run: (c, d) => c.rows.slice(0, -1).forEach((r, i) => { tr(r.rect, d, SPEED.short, i * 500).attr("width", r.width); show(r.text, d, i * 500); }) },
      { say: "The rest isn't explained by anything measured. A Fairlie decomposition describes; it doesn't say why.",
        run: (c, d) => { const r = c.rows[c.rows.length - 1]; tr(r.rect, d).attr("width", r.width); show(r.text, d); } },
    ],
  };

  // ---------------------------------------------------------------- parents (study results)
  SCENES.parents = {
    setup(svg) {
      const gap = (parent) => DATA.fathers.gaps.find((g) => g.parent === parent && g.group === "Not employed").gap;
      setHeading("Adjusted gap, not employed vs. full-time (percentage points)");
      const mothers = makeBar(svg, { x: 40, y: 90, width: 440, max: 8, color: COLOR.b, title: "Mothers", suffix: " pts" });
      const fathers = makeBar(svg, { x: 40, y: 160, width: 440, max: 8, color: COLOR.b, title: "Fathers", suffix: " pts" });
      return { gap, mothers, fathers };
    },
    beats: [
      { say: "Mothers who aren't employed report fair or poor mental health 2.8 points more often than full-time mothers.",
        run: (c, d) => c.mothers.to(c.gap("mothers"), d) },
      { say: "Fit the same model to fathers: their gap is more than twice as large, in line with research finding that being out of work weighs more on men.",
        run: (c, d) => c.fathers.to(c.gap("fathers"), d) },
    ],
  };

  // ================================================================ menu and player

  const ANALYSES = {
    main: [
      ["weights", "Weights", "Survey weights make each answer count for the number of children it stands for."],
      ["uncertainty", "Confidence intervals", "95% intervals by Taylor linearization, with the survey's strata and households."],
      ["logistic", "Logistic regression", "How the study's models turn yes/no answers into smooth chances."],
      ["models", "Adjusted models", "Survey-weighted logistic regression, M0 to M2."],
      ["margins", "Adjusted percentages", "Predictive margins: the scale every gap in the story is on."],
      ["imputations", "Six incomes", "Multiple imputation of income, combined with Rubin's rules."],
      ["interaction", "Age interaction", "Employment × child age, Wald χ²(6) = 20.2, p = .003."],
      ["reliability", "Reliability rules", "NSCH guidance on small groups."],
    ],
    exploratory: [
      ["under2", "Children under 2", "The hypothesis about full-time mothers of babies."],
      ["bothEnds", "Both ends of the scale", "Excellent or very good as well as fair or poor."],
      ["decomposition", "Gap decomposition", "Fairlie decomposition, averaged over 100 replications and six imputations."],
      ["parents", "Mothers vs. fathers", "The same model for fathers, and the gaps compared."],
    ],
  };

  function render(box) {
    box.innerHTML = `
      <div class="controls analysis-tabs" role="group" aria-label="Which analyses">
        <button type="button" class="pill" data-tab="main" aria-pressed="true">Main study</button>
        <button type="button" class="pill" data-tab="exploratory" aria-pressed="false">Exploratory</button>
      </div>
      <div class="controls s101-picks" role="group" aria-label="Pick a method"></div>
      <figure class="s101-figure">
        <span class="s101-tag"></span>
        <p class="s101-say" aria-live="polite"></p>
        <p class="s101-heading"></p>
        <div class="s101-stage">
          <div class="s101-toolbar">
            <p class="s101-hint">Zoom: + / −, pinch, or Ctrl + scroll. Drag, or focus the chart and use arrow keys, to look around.</p>
            <div class="s101-zoom" role="group" aria-label="Zoom">
              <button type="button" data-zoom="in" aria-label="Zoom in">+</button>
              <button type="button" data-zoom="out" aria-label="Zoom out">−</button>
              <button type="button" data-zoom="fit" aria-label="Show all">Fit</button>
            </div>
          </div>
          <svg class="s101-svg" viewBox="0 0 ${W} ${H}" role="img" tabindex="0"><g class="s101-world"></g></svg>
        </div>
        <div class="s101-extra"></div>
        <div class="s101-player">
          <button type="button" class="pill" data-go="back" aria-label="Previous step">◀</button>
          <button type="button" class="pill s101-play" data-go="play"></button>
          <button type="button" class="pill" data-go="next" aria-label="Next step">▶</button>
          <span class="s101-dots" aria-hidden="true"></span>
          <span class="s101-count"></span>
        </div>
        <figcaption class="s101-caption"></figcaption>
      </figure>
      <p class="cite">Tools: Python (pandas, NumPy, SciPy), a survey-regression module written for this project and checked against statsmodels, DuckDB SQL cross-checks, and D3.js for these graphics.</p>`;

    const $ = (selector) => box.querySelector(selector);
    const svgNode = $(".s101-svg");
    const world = d3.select(svgNode).select(".s101-world");
    const playButton = $(".s101-play");
    let scene = null;
    let beat = 0;
    let timer = null;
    let playing = false;

    // Zoom: Ctrl/⌘ + wheel, trackpad or two-finger pinch, or the buttons; drag to move.
    // A plain wheel or one-finger swipe still scrolls the page.
    const zoom = d3.zoom().scaleExtent([ZOOM.min, ZOOM.max])
      .filter((event) => {
        if (event.type === "wheel") {
          return event.ctrlKey || event.metaKey;
        }
        if (event.type.startsWith("touch")) {
          return event.touches.length > 1;
        }
        return !event.button;
      })
      .translateExtent([[0, 0], [W, H]])
      .on("zoom", (event) => world.attr("transform", event.transform));
    const svgSel = d3.select(svgNode).call(zoom);
    const zoomDuration = REDUCED ? 0 : SPEED.short;
    box.querySelectorAll("[data-zoom]").forEach((b) => b.addEventListener("click", () => {
      const how = b.dataset.zoom;
      const t = svgSel.transition().duration(zoomDuration);
      if (how === "fit") {
        t.call(zoom.transform, d3.zoomIdentity);
      } else {
        t.call(zoom.scaleBy, how === "in" ? ZOOM.step : 1 / ZOOM.step);
      }
    }));

    const PAN = 40;
    svgNode.addEventListener("keydown", (event) => {
      const k = d3.zoomTransform(svgNode).k;
      const moves = { ArrowLeft: [PAN, 0], ArrowRight: [-PAN, 0], ArrowUp: [0, PAN], ArrowDown: [0, -PAN] };
      if (moves[event.key]) {
        svgSel.call(zoom.translateBy, moves[event.key][0] / k, moves[event.key][1] / k);
      } else if (event.key === "+" || event.key === "=") {
        svgSel.call(zoom.scaleBy, ZOOM.step);
      } else if (event.key === "-") {
        svgSel.call(zoom.scaleBy, 1 / ZOOM.step);
      } else if (event.key === "0") {
        svgSel.call(zoom.transform, d3.zoomIdentity);
      } else {
        return;
      }
      event.preventDefault();
    });

    // Plays on its own only while on screen; quiet for screen readers while playing.
    let visible = false;

    function updatePlayLabel() {
      const last = beat === scene.beats.length - 1;
      playButton.textContent = playing ? "Pause ❚❚" : last ? "Replay ↻" : "Play ▶";
      $(".s101-say").setAttribute("aria-live", playing ? "off" : "polite");
    }

    function stop() {
      playing = false;
      clearTimeout(timer);
      updatePlayLabel();
    }

    function goTo(k, animate) {
      clearTimeout(timer);
      beat = Math.max(0, Math.min(scene.beats.length - 1, k));
      world.selectAll("*").interrupt().interrupt("morph").remove();
      const heading = $(".s101-heading");
      heading.textContent = "";
      setHeading = (text) => { heading.textContent = text; };
      $(".s101-extra").innerHTML = "";
      const ctx = scene.setup(world, $(".s101-extra"));
      for (let i = 0; i < beat; i += 1) {
        scene.beats[i].run(ctx, 0);
      }
      scene.beats[beat].run(ctx, animate && !REDUCED ? 1 : 0);
      $(".s101-say").textContent = scene.beats[beat].say;
      $(".s101-count").textContent = `${beat + 1} / ${scene.beats.length}`;
      $(".s101-dots").innerHTML = scene.beats.map((b, i) => `<i class="${i <= beat ? "on" : ""}"></i>`).join("");
      if (playing && beat < scene.beats.length - 1) {
        timer = setTimeout(() => goTo(beat + 1, true), PAUSE + SPEED.long);
      } else {
        playing = false;
      }
      updatePlayLabel();
    }

    function open(key, caption) {
      scene = SCENES[key];
      $(".s101-tag").textContent = scene.illustration ? "Illustration" : "Study results";
      $(".s101-caption").textContent = caption;
      svgNode.setAttribute("aria-label", caption);
      box.querySelectorAll(".s101-picks button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.key === key)));
      svgSel.call(zoom.transform, d3.zoomIdentity);
      playing = !REDUCED && visible;
      goTo(0, true);
    }

    box.querySelectorAll("[data-go]").forEach((b) => b.addEventListener("click", () => {
      const go = b.dataset.go;
      if (go === "play") {
        if (playing) {
          stop();
          return;
        }
        playing = true;
        goTo(beat === scene.beats.length - 1 ? 0 : beat + 1, true);
        return;
      }
      stop();
      goTo(beat + (go === "next" ? 1 : -1), true);
    }));

    function showTab(tab) {
      const picks = $(".s101-picks");
      picks.innerHTML = "";
      for (const [key, name, caption] of ANALYSES[tab]) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "pill";
        button.dataset.key = key;
        button.textContent = name;
        button.addEventListener("click", () => open(key, caption));
        picks.appendChild(button);
      }
      box.querySelectorAll("[data-tab]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.tab === tab)));
      open(ANALYSES[tab][0][0], ANALYSES[tab][0][2]);
    }
    box.querySelectorAll("[data-tab]").forEach((b) => b.addEventListener("click", () => showTab(b.dataset.tab)));

    // Drawn at once; starts playing when any part scrolls into view, stops when it leaves.
    showTab("main");
    let started = false;
    new IntersectionObserver((entries) => {
      visible = entries[entries.length - 1].isIntersecting;
      if (visible && !started && !REDUCED) {
        started = true;
        playing = true;
        goTo(0, true);
      } else if (!visible && playing) {
        stop();
      }
    }).observe(box);
  }

  document.querySelectorAll("[data-stats101]").forEach(render);
})();
