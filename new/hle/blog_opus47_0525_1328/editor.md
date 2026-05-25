## Story Spine

**Core claim**: Humanity's Last Exam is a wall against AI deliberately built from the full breadth of human expertise — 2,500 questions so hard that the best models of early 2025 scored in the single digits, assembled by nearly a thousand specialists each contributing their own narrow corner of knowledge.

**Tension**: We are used to AI acing every test we give it (90%+ on MMLU). HLE was engineered precisely so that wouldn't happen — and at launch it worked spectacularly: GPT-4o got 2.7%. But the wall is being scaled fast, and it isn't perfect (a chunk of answers may be wrong).

**Payoff**: After reading, you should (1) viscerally feel what "impossibly hard" looks like by seeing the actual questions, (2) understand that the difficulty is engineered, not accidental, and (3) hold both facts at once — the exam is a remarkable artifact of collective human expertise AND a fallible, fast-aging snapshot.

## Sections

### edt_01: Hook — Can you even understand the question?
**Evidence**: ana_05 | **Context**: det_03, det_07

[det_03] In early 2025, researchers gave the world's best AI models a new exam. GPT-4o scored 2.7%. Claude 3.5 Sonnet managed 4.1%. OpenAI's o1 — a model built specifically to reason — reached 8.0%. On most modern benchmarks these systems score above 90%. This one was different by design.

[editorial] It is called Humanity's Last Exam, and the fastest way to understand it is not to read about it. It is to try to answer one of its questions yourself.

[ana_05, det_07] Here are real questions from the exam — including the roughly one in seven (13.7%) that come with an image you must interpret to have any chance. Read one. Look at the picture. Then reveal the answer, and notice the gap between what you can do and what the question demands.

[CHART: none]
[MEDIA: interactive]

### edt_02: What HLE is and why it exists
**Evidence**: | **Context**: det_01, det_02

[det_02] HLE exists because our rulers for measuring AI stopped working. Large language models now score over 90% on popular benchmarks like MMLU, which makes those tests useless for telling one frontier model from another. Dan Hendrycks, who directs the Center for AI Safety, started the project after Elon Musk remarked that existing benchmarks were too easy.

[det_01] The answer was to build the hardest closed-ended academic test that humans could still write and grade. The Center for AI Safety and Scale AI assembled 2,500 questions across more than 100 subjects, contributed by nearly 1,000 subject-matter experts from over 500 institutions in 50 countries. Every question has a single, verifiable answer that cannot be found with a quick search.

[MEDIA: image]

### edt_03: The difficulty is engineered
**Evidence**: | **Context**: det_05, det_03

[det_05] The hardness is not luck. Experts competed for a $500,000 prize pool, and every submission was first thrown at frontier models. Only questions the models failed — or answered worse than random guessing — advanced. More than 70,000 model-evaluation attempts winnowed the pool to about 13,000 stumpers, which then passed two rounds of graduate-level human review before the final 2,500 were chosen.

[det_03] So every question in this dataset is, by construction, one that a machine could not answer and at least two human experts agreed was both correct and unambiguous. That is why the launch scores looked the way they did.

[CHART: none]
[MEDIA: video]

### edt_04: A math exam with seven appendices
**Evidence**: ana_03, ana_02 | **Context**: det_08

[ana_03] In headcount terms, HLE is a math exam. The 1,021 mathematics questions are 40.8% of the whole thing — 3.6 times the next-largest category. The other seven categories together make up the remaining 59.2%.

[ana_02, det_08] That lopsidedness is not an artifact of this snapshot: the category shares here match the figures HLE's creators publish almost exactly, none deviating by more than about a percentage point. Math 40.8%, Biology/Medicine 11.2%, Computer Science/AI 9.6%, then a cluster of mid-sized fields down to Engineering at 4.4%.

[CHART: ana_02]
[MEDIA: chart]

### edt_05: The long tail of human expertise
**Evidence**: ana_08, ana_09, ana_10 | **Context**: det_01, det_05

[ana_08] Beneath the eight tidy categories sit 193 distinct subjects, and they are wildly uneven. "Mathematics" alone is 863 questions (34.5% of the exam). But the tail is enormous: 147 subjects appear five times or fewer, and 83 subjects appear exactly once.

[ana_09] The people behind them tell the same story. The 2,109 attributed questions come from 579 named contributors. The most prolific wrote 99; but the top ten together account for only 22.1% of attributed questions, and fully half of all named authors (289 of 579) contributed exactly one. HLE is built on breadth, not on a handful of power users.

[ana_10] That breadth is most visible in the catch-all "Other" category (233 questions), where the exam stops feeling like STEM: Trivia, Musicology, Art History, Games, Chess, even Classical Ballet. This is where a mate-in-2 chess puzzle or a "name this anime opening" sits beside the polynomials.

[CHART: ana_08]
[MEDIA: chart]

### edt_06: The shape of an impossible question
**Evidence**: ana_06, ana_07, ana_04, ana_11 | **Context**: det_06, det_07

[ana_04, ana_11] Three-quarters of the exam (76.4%) is short-answer, not multiple choice — and short does not mean easy. Among those 1,909 exact-match questions the median answer is just 8 characters, and almost a third are three characters or fewer: a single number, letter or symbol. The answer is tiny and unforgiving; being one digit off scores zero.

[ana_06] The questions that need an image cluster in the hands-on fields. Engineering is the most visual (42.3% carry an image) and Chemistry next (38.8%), while Math — the biggest category — is the least visual at 4.4%.

[ana_07] Format tracks the field, too. Biology/Medicine is mostly multiple choice (59.3%), because diagnosis fits "which of these"; Math is almost all short answer (9.2% multiple choice), because a number can be graded exactly. How a field expresses an answer decides how HLE grades it.

[CHART: ana_06]
[MEDIA: chart]

### edt_07: The wall is being scaled — and it has cracks
**Evidence**: | **Context**: det_09, det_10

[det_09] HLE was built to last, but AI moves fast. Within about a year the scores climbed from the single digits into the mid-40s: as of May 2026 Gemini 3.1 Pro Preview leads at about 44.7%, GPT-5.4 at 41.6%. That is a stunning jump from o3-mini's 13.4% launch-day high — though it still leaves more than half the exam unsolved, and these tool-augmented figures are not directly comparable to the no-tools launch numbers.

[det_10] And the wall has cracks. In July 2025 the AI-science lab FutureHouse audited the text-only chemistry and biology questions and estimated that about 30% of those answers conflicted with the published literature; the HLE team ran its own checks and put the error rate nearer 18%. Either way, the lesson holds: the answers here are expert-reviewed but not infallible, and the subject labels are contributor-assigned. Treat HLE as a remarkable, fast-aging human artifact — not as ground truth.

[editorial] What makes Humanity's Last Exam worth your attention is exactly this doubleness. It is the most ambitious attempt yet to measure machine knowledge against the human frontier, assembled from a thousand specialists' hardest questions — and it is already being outrun, one corrected answer at a time.

[CHART: none]
[MEDIA: audio]

## Editorial Notes
- ana_05 (13.7% image rate) and det_03 (2.7% GPT-4o) must be exact — they anchor the hook.
- The real-question gallery (edt_01) is the load-bearing centerpiece. Show actual question images + question text + answer reveal, credited to the dataset and the contributing author.
- Keep the controversy (det_10, ~30% vs 18%) visible, not buried — it is the honesty beat and the close.
- Launch scores (det_03) and current scores (det_09) must be clearly distinguished as no-tools vs tool-augmented — do not blend them.
- Category shares (ana_02) must match official within ~1pp framing; do not overstate as the entire HLE (caveat_02).
- Math 40.8%, 3.6x, 193 subjects, 579 authors, 76.4% exactMatch — exact figures, no rounding drift.
