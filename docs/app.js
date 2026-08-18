
// CASE FILE 001 typing animation
const caseTag = document.getElementById("caseTag");

if (caseTag) {
  const fullText = caseTag.dataset.text || "CASE FILE 001";
  caseTag.textContent = "";

  let caseIndex = 0;

  function typeCaseFile() {
    if (caseIndex >= fullText.length) return;

    caseTag.textContent += fullText[caseIndex];
    caseIndex += 1;

    setTimeout(typeCaseFile, 72);
  }

  setTimeout(typeCaseFile, 280);
}

// Spotlight
document.addEventListener("mousemove", (event) => {
  document.documentElement.style.setProperty("--mouse-x", `${event.clientX}px`);
  document.documentElement.style.setProperty("--mouse-y", `${event.clientY}px`);
});

// Reveal
const revealTargets = document.querySelectorAll(
  ".exec-heading, .headline-grid article, .exec-skills article, .exec-block, .interactive-profile, .interactive-ranking-layout, .exec-conclusion"
);

revealTargets.forEach(el => el.classList.add("reveal"));

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      revealObserver.unobserve(entry.target);
    }
  });
}, {threshold: 0.10});

revealTargets.forEach(el => revealObserver.observe(el));

// Active navigation
const navLinks = [...document.querySelectorAll(".nav-links a")];
const navSections = navLinks
  .map(link => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

function updateActiveNav() {
  let current = null;

  navSections.forEach(section => {
    if (section.getBoundingClientRect().top <= 145) {
      current = section.id;
    }
  });

  navLinks.forEach(link => {
    link.classList.toggle(
      "active",
      link.getAttribute("href") === `#${current}`
    );
  });
}

window.addEventListener("scroll", updateActiveNav);
updateActiveNav();

// Interactive ranking demo
let rankingDemoData = null;
let currentDemoUser = null;
let currentDemoPolicy = "personalized";

const userSelect = document.getElementById("demo-user");
const policyButtons = document.querySelectorAll(".policy-button");

async function loadRankingDemo() {
  try {
    const response = await fetch("assets/ranking_demo.json");

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    rankingDemoData = await response.json();

    rankingDemoData.users.forEach(user => {
      const option = document.createElement("option");
      option.value = user.user_id;
      option.textContent = `User ${user.user_id} | ${user.preferred_category}`;
      userSelect.appendChild(option);
    });

    currentDemoUser = rankingDemoData.users[0];
    renderRankingDemo();

  } catch (error) {
    console.error("Could not load ranking demo:", error);

    const candidateList = document.getElementById("candidate-list");
    if (candidateList) {
      candidateList.innerHTML = `
        <div style="padding:16px;color:var(--muted);font:11px Arial,sans-serif">
          Demo data could not load. Keep your existing
          <code>docs/assets/ranking_demo.json</code> file when replacing the dashboard.
        </div>
      `;
    }
  }
}

function scoreKey() {
  return currentDemoPolicy === "baseline"
    ? "baseline_score"
    : "personalized_score";
}

function renderRankingDemo() {
  if (!currentDemoUser) return;

  document.getElementById("demo-primary").textContent =
    currentDemoUser.preferred_category;

  document.getElementById("demo-secondary").textContent =
    currentDemoUser.secondary_category;

  document.getElementById("demo-session").textContent =
    `${currentDemoUser.preferred_session_minutes} min`;

  document.getElementById("demo-novelty").textContent =
    Number(currentDemoUser.novelty_preference).toFixed(2);

  const key = scoreKey();

  const candidates = [...currentDemoUser.candidates]
    .sort((a, b) => b[key] - a[key]);

  document.getElementById("candidate-count").textContent =
    `${candidates.length} candidates`;

  const container = document.getElementById("candidate-list");
  container.innerHTML = "";

  candidates.forEach((candidate, index) => {
    const row = document.createElement("div");
    row.className = "candidate-row";

    if (index < 5) row.classList.add("top-five");

    const topFive = index < 5
      ? `<span class="top-five-label">TOP 5</span>`
      : "";

    row.innerHTML = `
      <div class="candidate-rank">#${index + 1}</div>

      <div class="candidate-info">
        <strong>
          ${candidate.experience_name}
          ${topFive}
        </strong>
        <span>${candidate.category}</span>
      </div>

      <div class="candidate-score">
        <strong>${(candidate[key] * 100).toFixed(1)}%</strong>
        <small>score</small>
      </div>
    `;

    row.addEventListener("click", () => {
      document.querySelectorAll(".candidate-row")
        .forEach(item => item.classList.remove("selected"));

      row.classList.add("selected");
      renderInspector(candidate, key);
    });

    container.appendChild(row);
  });

  if (candidates.length) {
    const first = container.querySelector(".candidate-row");
    first.classList.add("selected");
    renderInspector(candidates[0], key);
  }

  updatePolicyCopy();
}

function renderInspector(candidate, key) {
  document.getElementById("inspector-name").textContent =
    candidate.experience_name;

  document.getElementById("inspector-category").textContent =
    candidate.category;

  document.getElementById("inspector-score").textContent =
    `${(candidate[key] * 100).toFixed(1)}%`;

  document.getElementById("feature-primary").textContent =
    candidate.primary_category_match ? "Yes" : "No";

  document.getElementById("feature-secondary").textContent =
    candidate.secondary_category_match ? "Yes" : "No";

  document.getElementById("feature-quality").textContent =
    Number(candidate.quality_score).toFixed(2);

  document.getElementById("feature-popularity").textContent =
    Number(candidate.popularity_score).toFixed(2);

  document.getElementById("feature-novelty").textContent =
    Number(candidate.novelty_alignment).toFixed(2);

  document.getElementById("feature-session").textContent =
    `${candidate.avg_session_minutes} min`;
}

function updatePolicyCopy() {
  const title = document.getElementById("ranking-policy-title");
  const description = document.getElementById("ranking-policy-description");

  if (currentDemoPolicy === "baseline") {
    title.textContent = "Historical ranking";
    description.textContent =
      "Ranks experiences using past engagement performance without adapting the score to the individual user.";
  } else {
    title.textContent = "Personalized ranking";
    description.textContent =
      "Uses user preferences, experience features, and their match to predict meaningful engagement.";
  }
}

if (userSelect) {
  userSelect.addEventListener("change", () => {
    const selectedId = Number(userSelect.value);

    currentDemoUser = rankingDemoData.users.find(
      user => user.user_id === selectedId
    );

    renderRankingDemo();
  });
}

policyButtons.forEach(button => {
  button.addEventListener("click", () => {
    policyButtons.forEach(item => item.classList.remove("active"));
    button.classList.add("active");
    currentDemoPolicy = button.dataset.policy;
    renderRankingDemo();
  });
});

if (userSelect) loadRankingDemo();
