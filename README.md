# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

Student reviews and evaluations of CS Professors and courses at NC State University (NCSU).

This knowledge is valuable because official course catalogs describe *what* is taught but
never *how* — teaching style, grading transparency, exam difficulty, workload, and whether a
professor's office hours are actually useful. Students currently piece this together from scattered
Rate My Professors pages, Reddit threads, and word-of-mouth, with no single searchable source.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors, Coursicle – Vincent Freeh | Professor Review | https://www.ratemyprofessors.com/professor/1348612, https://www.coursicle.com/ncsu/?professor=Vincent+Freeh&type=reviews |
| 2 | Rate My Professors, Coursicle  – Thomas Price | Professor Review | https://www.ratemyprofessors.com/professor/2480706, https://www.coursicle.com/ncsu/?professor=Thomas+Price&type=reviews |
| 3 | Rate My Professors, Coursicle  – Sarah Heckman | Professor Review | https://www.ratemyprofessors.com/professor/1605846, https://www.coursicle.com/ncsu/?professor=Sarah+Heckman&type=reviews |
| 4 | Rate My Professors, Coursicle  - Kemafor Ogan | Professor Review | https://www.ratemyprofessors.com/professor/1295287, https://www.coursicle.com/ncsu/?professor=Kemafor+Ogan&type=reviews |
| 5 | Reddit Thread - NCSU for CS | Student Discussion | https://www.reddit.com/r/NCSU/comments/1pzwwe1/ncsu_for_csc_or_unc/, https://www.reddit.com/r/NCSU/comments/13l019t/does_anybody_have_some_experience_with_ncsu/, https://www.reddit.com/r/NCSU/comments/1su9yc8/how_is_compsci_in_ncsu/, https://www.reddit.com/r/NCSU/comments/p0206l/how_good_is_the_cs_program_at_nc_state/ |
| 6 | Reddit Thread - CSC 116 | Student Discussion | https://www.reddit.com/r/NCSU/comments/qtgusd/professors_for_csc_116/, https://www.reddit.com/r/NCSU/comments/17rj6nu/is_csc_116_a_difficult_class_if_you_have_limited/, https://www.reddit.com/r/NCSU/comments/hmi297/csc_116/ |
| 7 | Reddit Thread - CSC 216 | Student Discussion | https://www.reddit.com/r/NCSU/comments/1ru4cqg/csc_216_major_projects/, https://www.reddit.com/r/NCSU/comments/95lnv1/how_heavy_is_the_workload_for_csc_216/, https://www.reddit.com/r/NCSU/comments/eeeuh0/difficulty_of_csc_216/ |
| 8 | Reddit Thread - CSC 226 | Student Discussion | https://www.reddit.com/r/NCSU/comments/15yniwm/csc_226/, https://www.reddit.com/r/NCSU/comments/1nklgtm/how_hard_are_the_csc226_exams/, https://www.reddit.com/r/NCSU/comments/kc2la1/csc_226/ |
| 9 | Reddit Thread - CSC 326 | Student Discussion | https://www.reddit.com/r/NCSU/comments/ebyanw/csc_majors_what_makes_csc326_software_engineering/, https://www.reddit.com/r/NCSU/comments/onnz1l/question_about_csc326/, https://www.reddit.com/r/NCSU/comments/8fsymq/csc_326_final/ |
| 10 | Reddit Thread - CSC 520 | Student Discussion | https://www.reddit.com/r/NCSU/comments/k38f2u/csc_520ai_1_with_dr_bita_akram/, https://www.reddit.com/r/NCSU/comments/k9xc41/has_anyone_taken_csc_520_artificial_intelligence/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
