/* "A snapshot, not the whole story": an interactive illustration of what the
   survey can and cannot show. Each part opens a note drawing on the study's
   findings (docs/conclusions.md) and the literature (docs/literature-review.md).
   Drawn into every [data-snapshot]. All content is static text written here. */

(function () {
  "use strict";

  const NOTES = {
    photo: {
      title: "What the snapshot shows",
      body: "Mothers looking for work are about twice as likely as full-time mothers to report fair or poor mental health, and less likely to report excellent or very good. Part-time and full-time mothers look the same. Full-time mothers of babies are not worse off.",
      cite: "This study, NSCH 2023–2025",
    },
    before: {
      title: "Before: how did they get here?",
      body: "Studies that follow mothers over years find that continuous full-time work after a first birth goes with better health at 40, and persistent unemployment with the worst.",
      cite: "Frech & Damaske (2012)",
    },
    after: {
      title: "After: what happens next?",
      body: "Health also shapes work: in a two-wave U.S. study, better physical functioning predicted getting or keeping a full-time job.",
      cite: "Ross & Mirowsky (1995)",
    },
    loop: {
      title: "Which shapes which?",
      body: "Unemployed adults report more distress on average, yet people who lost jobs only because their plant closed showed no drop in mental health, which suggests that poorer health also leads people out of work.",
      cite: "Paul & Moser (2009); Schmitz (2011)",
    },
    hours: {
      title: "Work hours and schedules",
      body: "When hours are measured, more hours at 6 months after a birth go with more depressive symptoms and parenting stress.",
      cite: "Chatterji, Markowitz & Brooks-Gunn (2013)",
    },
    postpartum: {
      title: "Postpartum depression and anxiety",
      body: "With a depression scale, the length of maternity leave shows a U-shape: the fewest symptoms at about six months of leave. The National Health Interview Survey (PHQ-8, GAD-7) could test this survey's question better.",
      cite: "Dagher, McGovern & Dowd (2014)",
    },
    return: {
      title: "When mothers went back to work",
      body: "Among mothers who worked full-time before birth, returning within 12 weeks went with more depressive symptoms, and paid leave helped those who returned early.",
      cite: "Mandal (2018)",
    },
    quality: {
      title: "Job quality and flexibility",
      body: "Work–family conflict 11 weeks after birth went with worse mental health, in a dose–response pattern. Employment status alone hides these differences.",
      cite: "Grice et al. (2007)",
    },
    childcare: {
      title: "Child care",
      body: "In this survey, families of mothers of babies who weren't working full-time were two to four times as likely to report a job change because of child care. Research finds child care costs shape whether and how much mothers work.",
      cite: "This study; Morrissey (2017)",
    },
  };

  const SHOWS = ["Working full-time, part-time or not at all", "One rating of mental health", "The child's age"];
  const MISSING = [
    ["hours", "Work hours and schedules"],
    ["postpartum", "Postpartum depression and anxiety"],
    ["return", "When mothers went back to work"],
    ["quality", "Job quality and flexibility"],
    ["childcare", "Child care costs"],
  ];

  const SCENE = `
    <svg class="snap-scene" viewBox="0 0 240 160" aria-hidden="true">
      <rect class="scene-wall" width="240" height="160"/>
      <rect class="scene-window" x="150" y="18" width="62" height="54" rx="3"/>
      <path class="scene-window-bar" d="M181 18V72M150 45H212"/>
      <rect class="scene-table" x="20" y="112" width="200" height="6" rx="3"/>
      <rect class="scene-laptop" x="44" y="90" width="38" height="22" rx="2"/>
      <rect class="scene-laptop" x="38" y="111" width="50" height="3" rx="1.5"/>
      <circle class="scene-parent" cx="112" cy="58" r="13"/>
      <path class="scene-parent" d="M92 112V86Q92 74 112 74Q132 74 132 86V112Z"/>
      <circle class="scene-child" cx="160" cy="88" r="9"/>
      <path class="scene-child" d="M147 112V102Q147 96 160 96Q173 96 173 102V112Z"/>
      <path class="scene-bubble" d="M120 22h44a6 6 0 0 1 6 6v14a6 6 0 0 1-6 6h-30l-8 8v-8h-6a6 6 0 0 1-6-6V28a6 6 0 0 1 6-6Z"/>
      <text class="scene-bubble-text" x="142" y="39" text-anchor="middle">Good</text>
    </svg>`;

  const GHOST = `
    <svg class="snap-ghost-art" viewBox="0 0 240 160" aria-hidden="true">
      <circle class="ghost-shape" cx="112" cy="58" r="13"/>
      <path class="ghost-shape" d="M92 112V86Q92 74 112 74Q132 74 132 86V112Z"/>
      <text class="ghost-mark" x="170" y="96" text-anchor="middle">?</text>
    </svg>`;

  const LOOP = `
    <svg class="snap-loop-arrows" viewBox="0 0 120 60" aria-hidden="true">
      <path class="loop-arrow" d="M8 22Q60 -4 112 22"/>
      <path class="loop-head" d="M104 14L112 22L101 25"/>
      <path class="loop-arrow" d="M112 38Q60 64 8 38"/>
      <path class="loop-head" d="M16 46L8 38L19 35"/>
      <text class="loop-mark" x="60" y="36" text-anchor="middle">?</text>
    </svg>`;

  const PIECE = `
    <svg class="snap-piece" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M4 7h4a2.5 2.5 0 1 1 5 0h4v4a2.5 2.5 0 1 1 0 5v4h-4a2.5 2.5 0 1 0-5 0H4v-4a2.5 2.5 0 1 0 0-5Z"/>
    </svg>`;

  function render(box) {
    box.innerHTML = `
      <figure class="snapshot" aria-label="What the survey can and cannot show">
        <p class="framing-lead">Tap any part of the picture to see what research says about it.</p>
        <div class="snap-row">
          <button type="button" class="snap-ghost snap-ghost-before" data-note="before">${GHOST}<strong>Before?</strong><span>How did they get here?</span></button>
          <button type="button" class="snap-polaroid" data-note="photo">
            ${SCENE}
            <strong class="snap-caption">One moment, 2023–2025</strong>
            <span class="snap-shows">${SHOWS.map((s) => `<span>${s}</span>`).join("")}</span>
          </button>
          <button type="button" class="snap-ghost snap-ghost-after" data-note="after">${GHOST}<strong>After?</strong><span>What happens next?</span></button>
        </div>
        <button type="button" class="snap-loop" data-note="loop">
          <span class="snap-node">Work</span>${LOOP}<span class="snap-node">Mental health</span>
        </button>
        <div class="snap-missing">
          <p class="snap-heading">Outside the frame</p>
          <div class="snap-pieces">
            ${MISSING.map(([key, label]) => `<button type="button" class="snap-missing-item" data-note="${key}">${PIECE}<span>${label}</span></button>`).join("")}
          </div>
        </div>
        <div class="snap-note-panel" aria-live="polite"></div>
      </figure>`;

    const panel = box.querySelector(".snap-note-panel");
    const buttons = box.querySelectorAll("[data-note]");
    function show(key) {
      const note = NOTES[key];
      panel.innerHTML = `<h3>${note.title}</h3><p>${note.body}</p><p class="cite">${note.cite}</p>`;
      buttons.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.note === key)));
    }
    buttons.forEach((b) => b.addEventListener("click", () => show(b.dataset.note)));
    show("photo");
  }

  document.querySelectorAll("[data-snapshot]").forEach(render);
})();
