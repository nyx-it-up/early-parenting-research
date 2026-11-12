/* Interactive introduction and methodology, drawn into [data-intro].
   Research and numbers come from docs/conclusions.md and
   docs/literature-review.md. All content is static text written here. */

(function () {
  "use strict";

  const THEORIES = {
    strain: {
      label: "Role strain",
      tilt: 14,
      extra: false,
      text: "Every role takes time and energy, and both are limited. Add a full-time job to caring for a baby, and something has to give.",
      prediction: "Prediction: full-time working mothers of young children struggle most.",
      cite: "Goode (1960)",
    },
    enhancement: {
      label: "Role enhancement",
      tilt: 0,
      extra: true,
      text: "Roles also bring resources: income, adult company, a sense of purpose. Within limits, more roles can make each one easier to carry.",
      prediction: "Prediction: employed mothers do as well as, or better than, mothers out of work.",
      cite: "Sieber (1974); Barnett & Hyde (2001)",
    },
  };

  const FINDINGS = [
    {
      title: "On average, paid work doesn't harm women's mental health",
      body: "A review of five decades of research found no adverse effect of employment on women's well-being, while noting that healthier women are also more likely to work.",
      cite: "Klumb & Lampert (2004)",
    },
    {
      title: "But the months after a birth may be different",
      body: "In a U.S. cohort, more work hours when the baby was 6 months old went with more depressive symptoms and parenting stress. Returning to work very early has also been linked to more symptoms.",
      cite: "Chatterji, Markowitz & Brooks-Gunn (2013); Mandal (2018)",
    },
    {
      title: "Being out of work goes with more distress, especially for men",
      body: "Meta-analyses find unemployed adults report more psychological problems (34% vs. 16%), with larger differences for men.",
      cite: "Paul & Moser (2009); McKee-Ryan et al. (2005)",
    },
  ];

  const FUNNEL = [
    { n: 151676, label: "Children sampled", detail: "The National Survey of Children's Health samples one child per household, every year. 2023, 2024 and 2025 are combined." },
    { n: 99011, label: "The adult who answered is a woman", detail: "The adult who knows the child best fills in the survey, including a question about their own mental health." },
    { n: 90415, label: "She is the child's mother", detail: "Biological or adoptive mothers only. Grandmothers, foster and step-mothers are left out, because their situations differ." },
    { n: 88047, label: "She answered both key questions", detail: "Left out: 1,361 mothers working without pay and 1,007 with no answer on work or mental health. These 88,047 mothers are every circle in The Room." },
    { n: 87318, label: "Used in the adjusted models", detail: "Models also need marital status, age and physical health; 729 more mothers are missing one of them." },
  ];

  const METHODS = [
    { label: "Weights", detail: "Some families are more likely to be sampled than others. Survey weights make each answer count for the number of U.S. children it stands for, so percentages describe the country, not just the sample." },
    { label: "Survey design", detail: "Uncertainty (the 95% confidence intervals) accounts for how the sample was drawn: by state and stratum, one child per household." },
    { label: "Income, six ways", detail: "About one in five families didn't report full income, so the Census Bureau filled it in six times. Every model runs on all six, and the results are combined." },
    { label: "Adjusted comparisons", detail: "Logistic regression compares mothers with similar income, education, marital status, number of children and age, so a gap can't simply reflect those differences." },
    { label: "Associations only", detail: "Everything is measured once, at the same time. The study shows which groups differ, not what causes the difference." },
  ];

  // A balance: the beam tilts under role strain and levels when resources are added.
  const BALANCE = `
    <svg class="balance" viewBox="0 0 320 170" aria-hidden="true">
      <path class="balance-stand" d="M160 70V150M120 150H200"/>
      <g class="balance-beam">
        <path class="balance-bar" d="M50 70H270"/>
        <path class="balance-string" d="M60 70L44 108M60 70L76 108M260 70L244 108M260 70L276 108"/>
        <path class="balance-pan" d="M36 108H84Q60 124 36 108Z"/>
        <path class="balance-pan" d="M236 108H284Q260 124 236 108Z"/>
        <g class="balance-load">
          <rect x="40" y="86" width="40" height="20" rx="3"/><text x="60" y="100">Work</text>
          <rect x="40" y="62" width="40" height="22" rx="3"/><text x="60" y="77">Kids</text>
        </g>
        <g class="balance-resources">
          <rect x="236" y="86" width="48" height="20" rx="3"/><text x="260" y="100">Income</text>
          <rect x="236" y="62" width="48" height="22" rx="3"/><text x="260" y="77">Support</text>
        </g>
      </g>
      <circle class="balance-pivot" cx="160" cy="70" r="5"/>
    </svg>`;

  function button(label, extra = "") {
    return `<button type="button" class="pill" ${extra}>${label}</button>`;
  }

  function render(box) {
    box.innerHTML = `
      <section class="framing" aria-label="Introduction and methods">
        <h2>Two ideas about working mothers</h2>
        <div class="theory">
          <div class="controls theory-switch" role="group" aria-label="Choose an idea">
            ${Object.entries(THEORIES).map(([key, t]) => button(t.label, `data-theory="${key}" aria-pressed="false"`)).join("")}
          </div>
          ${BALANCE}
          <div class="theory-text" aria-live="polite"></div>
        </div>

        <h3 class="framing-sub">What earlier research found</h3>
        <div class="findings">
          ${FINDINGS.map((f) => `<details class="finding"><summary>${f.title}</summary><p>${f.body}</p><p class="cite">${f.cite}</p></details>`).join("")}
        </div>

        <h2>How the study works</h2>
        <p class="framing-lead">Tap a step to see who is in, and who is left out.</p>
        <div class="funnel" role="list">
          ${FUNNEL.map((f, i) => `
            <div role="listitem" class="funnel-item"><button type="button" class="funnel-step" data-step="${i}" aria-pressed="false"
                    style="--share: ${(f.n / FUNNEL[0].n).toFixed(4)}">
              <span class="funnel-bar"></span>
              <span class="funnel-number">${f.n.toLocaleString("en-US")}</span>
              <span class="funnel-label">${f.label}</span>
            </button></div>`).join("")}
        </div>
        <p class="funnel-detail" aria-live="polite"></p>
        <div class="controls method-chips" role="group" aria-label="Methods">
          ${METHODS.map((m, i) => button(m.label, `data-method="${i}" aria-pressed="false"`)).join("")}
        </div>
        <p class="method-detail" aria-live="polite">Tap a method to learn what it does.</p>

        <h3 class="framing-sub">The analyses</h3>
        <div class="stats101" data-stats101></div>
      </section>`;

    const svg = box.querySelector(".balance");
    const theoryText = box.querySelector(".theory-text");
    function showTheory(key) {
      const t = THEORIES[key];
      svg.style.setProperty("--tilt", `${-t.tilt}deg`);
      svg.classList.toggle("show-resources", t.extra);
      theoryText.innerHTML = `<p>${t.text}</p><p><strong>${t.prediction}</strong></p><p class="cite">${t.cite}</p>`;
      box.querySelectorAll("[data-theory]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.theory === key)));
    }
    box.querySelectorAll("[data-theory]").forEach((b) => b.addEventListener("click", () => showTheory(b.dataset.theory)));
    showTheory("strain");

    const funnelDetail = box.querySelector(".funnel-detail");
    function showStep(i) {
      funnelDetail.textContent = FUNNEL[i].detail;
      box.querySelectorAll(".funnel-step").forEach((b) => b.setAttribute("aria-pressed", String(Number(b.dataset.step) === i)));
    }
    box.querySelectorAll(".funnel-step").forEach((b) => b.addEventListener("click", () => showStep(Number(b.dataset.step))));
    showStep(0);

    const methodDetail = box.querySelector(".method-detail");
    box.querySelectorAll("[data-method]").forEach((b) => b.addEventListener("click", () => {
      methodDetail.textContent = METHODS[Number(b.dataset.method)].detail;
      box.querySelectorAll("[data-method]").forEach((o) => o.setAttribute("aria-pressed", String(o === b)));
    }));
  }

  document.querySelectorAll("[data-intro]").forEach((box) => {
    render(box);
  });
})();
