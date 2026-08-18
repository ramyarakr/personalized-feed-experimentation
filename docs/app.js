// =========================================================
// Mouse spotlight
// =========================================================

document.addEventListener(
    "mousemove",
    (event) => {

        document.documentElement.style.setProperty(
            "--mouse-x",
            `${event.clientX}px`
        );

        document.documentElement.style.setProperty(
            "--mouse-y",
            `${event.clientY}px`
        );

    }
);


// =========================================================
// Scroll reveal
// =========================================================

const revealSelectors = [
    ".section-heading",
    ".case-question",
    ".process-step",
    ".evidence-card",
    ".note-card",
    ".finding-card",
    ".finding-summary",
    ".mini-stats",
    ".suspect-card",
    ".ranking-results",
    ".experiment-arm",
    ".experiment-middle",
    ".aa-validation",
    ".profile-card",
    ".pipeline-box",
    ".system-card",
    ".monitoring-chain",
    ".failure-file",
    ".skill-file",
    ".final-file"
];


const revealElements =
    document.querySelectorAll(
        revealSelectors.join(",")
    );


revealElements.forEach(
    (element) => {

        element.classList.add(
            "reveal"
        );

    }
);


const revealObserver =
    new IntersectionObserver(

        (entries) => {

            entries.forEach(
                (entry) => {

                    if (
                        entry.isIntersecting
                    ) {

                        entry.target.classList.add(
                            "visible"
                        );

                        revealObserver.unobserve(
                            entry.target
                        );

                    }

                }
            );

        },

        {
            threshold: 0.12
        }

    );


revealElements.forEach(
    (element) => {

        revealObserver.observe(
            element
        );

    }
);


// =========================================================
// Ranking result animation
// =========================================================

const rankingBars =
    document.querySelectorAll(
        ".result-fill"
    );


const rankingObserver =
    new IntersectionObserver(

        (entries) => {

            entries.forEach(
                (entry) => {

                    if (
                        !entry.isIntersecting
                    ) {
                        return;
                    }

                    const bar =
                        entry.target;

                    const width =
                        bar.dataset.width;

                    bar.style.width =
                        `${width}%`;

                    rankingObserver.unobserve(
                        bar
                    );

                }
            );

        },

        {
            threshold: 0.5
        }

    );


rankingBars.forEach(
    (bar) => {

        rankingObserver.observe(
            bar
        );

    }
);


// =========================================================
// Small paper tilt interaction
// =========================================================

const paperCards =
    document.querySelectorAll(
        [
            ".evidence-card",
            ".suspect-card",
            ".profile-card",
            ".failure-file"
        ].join(",")
    );


paperCards.forEach(
    (card) => {

        card.addEventListener(
            "mousemove",
            (event) => {

                if (
                    window.innerWidth < 800
                ) {
                    return;
                }

                const rect =
                    card.getBoundingClientRect();

                const x =
                    event.clientX
                    - rect.left;

                const y =
                    event.clientY
                    - rect.top;

                const rotateY =
                    (
                        x / rect.width
                        - 0.5
                    ) * 2;

                const rotateX =
                    (
                        0.5
                        - y / rect.height
                    ) * 2;

                card.style.transform =
                    `
                    perspective(700px)
                    rotateX(${rotateX}deg)
                    rotateY(${rotateY}deg)
                    translateY(-2px)
                    `;

            }
        );


        card.addEventListener(
            "mouseleave",
            () => {

                card.style.transform =
                    "";

            }
        );

    }
);


// =========================================================
// Active navigation
// =========================================================

const navLinks =
    document.querySelectorAll(
        ".nav-links a"
    );


const navSections =
    [...navLinks]
    .map((link) => {

        const id =
            link.getAttribute("href");

        return document.querySelector(id);

    })
    .filter(Boolean);


function updateActiveNav() {

    let current = null;

    navSections.forEach(
        (section) => {

            const top =
                section.getBoundingClientRect().top;

            if (top <= 170) {
                current = section.id;
            }

        }
    );


    navLinks.forEach(
        (link) => {

            const active =
                link.getAttribute("href")
                === `#${current}`;

            link.style.color =
                active
                    ? "var(--red-bright)"
                    : "";

        }
    );

}


window.addEventListener(
    "scroll",
    updateActiveNav
);


updateActiveNav();


// =========================================================
// Case file typing effect
// =========================================================

const caseTag =
    document.querySelector(
        ".case-tag"
    );


if (caseTag) {

    const fullText =
        caseTag.textContent.trim();

    caseTag.textContent = "";

    let index = 0;


    const typeCaseNumber = () => {

        if (
            index >= fullText.length
        ) {
            return;
        }

        caseTag.textContent +=
            fullText[index];

        index += 1;

        setTimeout(
            typeCaseNumber,
            65
        );

    };


    setTimeout(
        typeCaseNumber,
        300
    );

}


// =========================================================
// Slight parallax for case summary
// =========================================================

const caseSummary =
    document.querySelector(
        ".case-summary"
    );


window.addEventListener(
    "scroll",
    () => {

        if (
            !caseSummary
            || window.innerWidth < 900
        ) {
            return;
        }

        const amount =
            Math.min(
                window.scrollY * 0.035,
                18
            );

        caseSummary.style.translate =
            `0 ${amount}px`;

    }
);

// =========================================================
// INTERACTIVE RANKING EXPLAINER
// =========================================================

let rankingDemoData = null;

let currentDemoUser = null;

let currentDemoPolicy =
    "personalized";


const userSelect =
    document.getElementById(
        "demo-user"
    );


const policyButtons =
    document.querySelectorAll(
        ".policy-button"
    );


async function loadRankingDemo() {

    try {

        const response =
            await fetch(
                "assets/ranking_demo.json"
            );


        rankingDemoData =
            await response.json();


        rankingDemoData.users.forEach(
            (user) => {

                const option =
                    document.createElement(
                        "option"
                    );


                option.value =
                    user.user_id;


                option.textContent =
                    `User ${user.user_id} | ${user.preferred_category}`;


                userSelect.appendChild(
                    option
                );

            }
        );


        currentDemoUser =
            rankingDemoData.users[0];


        renderRankingDemo();


    } catch (error) {

        console.error(
            "Could not load ranking demo:",
            error
        );

    }

}


function getScoreKey() {

    if (
        currentDemoPolicy
        === "baseline"
    ) {

        return "baseline_score";

    }


    return "personalized_score";

}


function renderRankingDemo() {

    if (!currentDemoUser) {
        return;
    }


    // -----------------------------------------------------
    // User profile
    // -----------------------------------------------------

    document.getElementById(
        "demo-primary"
    ).textContent =
        currentDemoUser
            .preferred_category;


    document.getElementById(
        "demo-secondary"
    ).textContent =
        currentDemoUser
            .secondary_category;


    document.getElementById(
        "demo-session"
    ).textContent =
        `${currentDemoUser.preferred_session_minutes} min`;


    document.getElementById(
        "demo-novelty"
    ).textContent =
        currentDemoUser
            .novelty_preference
            .toFixed(2);


    // -----------------------------------------------------
    // Sort candidate pool
    // -----------------------------------------------------

    const scoreKey =
        getScoreKey();


    const candidates =
        [
            ...currentDemoUser
                .candidates
        ]
        .sort(
            (a, b) =>
                b[scoreKey]
                - a[scoreKey]
        );


    const container =
        document.getElementById(
            "candidate-list"
        );


    container.innerHTML = "";


    document.getElementById(
        "candidate-count"
    ).textContent =
        `${candidates.length} candidates`;


    candidates.forEach(
        (candidate, index) => {

            const row =
                document.createElement(
                    "div"
                );


            row.className =
                "candidate-row";


            if (index < 5) {

                row.classList.add(
                    "top-five"
                );

            }


            const topFiveLabel =
                index < 5
                ? `<span class="top-five-label">TOP 5</span>`
                : "";


            row.innerHTML = `
                <div class="candidate-rank">
                    #${index + 1}
                </div>

                <div class="candidate-info">

                    <strong>
                        ${candidate.experience_name}
                        ${topFiveLabel}
                    </strong>

                    <span>
                        ${candidate.category}
                    </span>

                </div>

                <div class="candidate-score">

                    <strong>
                        ${(
                            candidate[scoreKey]
                            * 100
                        ).toFixed(1)}%
                    </strong>

                    <small>
                        score
                    </small>

                </div>
            `;


            row.addEventListener(
                "click",
                () => {

                    document
                        .querySelectorAll(
                            ".candidate-row"
                        )
                        .forEach(
                            (item) => {

                                item.classList.remove(
                                    "selected"
                                );

                            }
                        );


                    row.classList.add(
                        "selected"
                    );


                    renderInspector(
                        candidate,
                        scoreKey
                    );

                }
            );


            container.appendChild(
                row
            );

        }
    );


    // Automatically inspect rank 1

    if (candidates.length > 0) {

        const firstRow =
            container.querySelector(
                ".candidate-row"
            );


        firstRow.classList.add(
            "selected"
        );


        renderInspector(
            candidates[0],
            scoreKey
        );

    }


    updatePolicyExplanation();

}


function renderInspector(
    candidate,
    scoreKey
) {

    document.getElementById(
        "inspector-name"
    ).textContent =
        candidate.experience_name;


    document.getElementById(
        "inspector-category"
    ).textContent =
        candidate.category;


    document.getElementById(
        "inspector-score"
    ).textContent =
        `${(
            candidate[scoreKey]
            * 100
        ).toFixed(1)}%`;


    document.getElementById(
        "feature-primary"
    ).textContent =
        candidate.primary_category_match
            ? "Yes"
            : "No";


    document.getElementById(
        "feature-secondary"
    ).textContent =
        candidate.secondary_category_match
            ? "Yes"
            : "No";


    document.getElementById(
        "feature-quality"
    ).textContent =
        candidate
            .quality_score
            .toFixed(2);


    document.getElementById(
        "feature-popularity"
    ).textContent =
        candidate
            .popularity_score
            .toFixed(2);


    document.getElementById(
        "feature-novelty"
    ).textContent =
        candidate
            .novelty_alignment
            .toFixed(2);


    document.getElementById(
        "feature-session"
    ).textContent =
        `${candidate.avg_session_minutes} min`;

}


function updatePolicyExplanation() {

    const title =
        document.getElementById(
            "ranking-policy-title"
        );


    const description =
        document.getElementById(
            "ranking-policy-description"
        );


    if (
        currentDemoPolicy
        === "baseline"
    ) {

        title.textContent =
            "Historical ranking";

        description.textContent =
            "Ranks experiences using past engagement performance without adapting the score to the individual user.";

            } else {

        title.textContent =
            "Personalized ranking";

        description.textContent =
            "Uses user preferences, experience features, and their match to predict meaningful engagement.";

    }

}


// =========================================================
// User change
// =========================================================

if (userSelect) {

    userSelect.addEventListener(
        "change",
        () => {

            const selectedId =
                Number(
                    userSelect.value
                );


            currentDemoUser =
                rankingDemoData.users.find(
                    (user) =>
                        user.user_id
                        === selectedId
                );


            renderRankingDemo();

        }
    );

}


// =========================================================
// Policy switch
// =========================================================

policyButtons.forEach(
    (button) => {

        button.addEventListener(
            "click",
            () => {

                policyButtons.forEach(
                    (item) => {

                        item.classList.remove(
                            "active"
                        );

                    }
                );


                button.classList.add(
                    "active"
                );


                currentDemoPolicy =
                    button.dataset.policy;


                renderRankingDemo();

            }
        );

    }
);


// =========================================================
// Initialize
// =========================================================

if (userSelect) {

    loadRankingDemo();

}