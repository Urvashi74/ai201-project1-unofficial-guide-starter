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
Rate My Professors pages, Reddit threads, and word-of-mouth, with no single searchable source. This would save prospective students hours of research and help them figure out their queries quickly. 

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
| 5 | Rate My Professors, Coursicle  - John-Paul Ore | Professor Review | https://www.ratemyprofessors.com/professor/2694467, https://www.coursicle.com/ncsu/?professor=John-Paul+Ore&type=reviews |
| 6 | Reddit Thread - CSC 116 | Student Discussion | https://www.reddit.com/r/NCSU/comments/qtgusd/professors_for_csc_116/, https://www.reddit.com/r/NCSU/comments/17rj6nu/is_csc_116_a_difficult_class_if_you_have_limited/, https://www.reddit.com/r/NCSU/comments/hmi297/csc_116/ |
| 7 | Reddit Thread - CSC 216 | Student Discussion | https://www.reddit.com/r/NCSU/comments/1ru4cqg/csc_216_major_projects/, https://www.reddit.com/r/NCSU/comments/95lnv1/how_heavy_is_the_workload_for_csc_216/, https://www.reddit.com/r/NCSU/comments/eeeuh0/difficulty_of_csc_216/ |
| 8 | Reddit Thread - CSC 226 | Student Discussion | https://www.reddit.com/r/NCSU/comments/15yniwm/csc_226/, https://www.reddit.com/r/NCSU/comments/1nklgtm/how_hard_are_the_csc226_exams/, https://www.reddit.com/r/NCSU/comments/kc2la1/csc_226/ |
| 9 | Reddit Thread - CSC 326 | Student Discussion | https://www.reddit.com/r/NCSU/comments/ebyanw/csc_majors_what_makes_csc326_software_engineering/, https://www.reddit.com/r/NCSU/comments/onnz1l/question_about_csc326/, https://www.reddit.com/r/NCSU/comments/8fsymq/csc_326_final/ |
| 10 | Reddit Thread - CSC 520 | Student Discussion | https://www.reddit.com/r/NCSU/comments/k38f2u/csc_520ai_1_with_dr_bita_akram/, https://www.reddit.com/r/NCSU/comments/k9xc41/has_anyone_taken_csc_520_artificial_intelligence/, https://www.reddit.com/r/NCSU/comments/ospvuo/advice_for_csc_520_artificial_intelligence/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
I used one review or comment per chunk — variable size, roughly 150–1500 characters — with no fixed character cap. Chunks are bounded by the `=== REVIEW N ===` / `=== COMMENT N ===` delimiters already present in each source file.

**Overlap:**
I used zero overlap. Each review is a self-contained student opinion, so there is no context that needs to flow across chunk boundaries. The only shared context (which professor or course a review belongs to) is handled through structured metadata fields rather than text overlap.

**Why these choices fit your documents:**
I chose delimiter-based chunking because each document in `documents/` is already structured as discrete review or comment blocks. Each block is one student's opinion — the natural unit of retrieval. Splitting on these markers gives one sentiment, one topic, and one professor/course per vector, which produces a cleaner embedding signal than arbitrary fixed-length cuts. I stripped the per-review metadata lines (course, quality, difficulty, grade, etc.) from the embedded chunk text to reduce noise, keeping only the review body and tags.

**Final chunk count:**
138 chunks across all 10 documents.

**Sample chunks (5 random):**

```
[CSC_326.txt #8] prof=None course=CSC 326 quality=None grade=None
size: 442 chars
text:
In CSC 326 the majority of points come from following their very specific processes and GitHub wiki
requirements exactly as written. During one project, a group wasn't able to implement any of the
requirements but still got an okay grade because they followed all the guidelines closely. A friend
got a terrible grade even though their group's code worked flawlessly because they ignored the git
guidelines. Follow all the guidelines exactly.

[RMP_Kemafor_Ogan.txt #12] prof=Kemafor Anyanwu Ogan course=CSC 541 quality=1.0 grade=None
size: 364 chars
text:
In-class activities and exams were pretty easy for advanced data structures. The struggle came with
the projects (that were very obviously not written by Dr. Ogan, but rather by a teacher that actually
taught the class). Dr. Ogan lacked teaching abilities -- could barely finish sentences, give any help
when instructions were unclear, and came across as stuck up.

[RMP_Kemafor_Ogan.txt #13] prof=Kemafor Anyanwu Ogan course=CSC 540 quality=1.0 grade=A
size: 351 chars
text:
Professor Kemafor is often underprepared for her classes as we can see her get confused all the time.
The concepts that she intends to explain are also not up to the mark as it's very tedious to listen
to her class. The questions that are given in the exams are of higher level and difficulty compared
to what is taught in class. Overall disappointed.

[RMP_Sarah_Heckman.txt #10] prof=Sarah Heckman course=CSC 216 quality=4.0 grade=A
size: 346 chars
text:
Dr. Heckman is a great lecturer and very enthusiastic, but the class overall is rough + fast-paced.
The exams are more difficult than they should be, especially the final (too much writing code by
hand). The projects take up lots of your time but are great at giving a hands-on experience, unlike
the slides. Beware of the min grade requirement!!

[RMP_Sarah_Heckman.txt #13] prof=Sarah Heckman course=CSC 216 quality=5.0 grade=A-
size: 333 chars
text:
Dr. Heckman is the best professor you can take for 216. She is really passionate about Java data
structures and techniques (especially iterators), and prepares you the best she can for the numerous
projects and coding assignments. Start Part 2 of the projects as soon as you can -- you will spend
more time than you expect debugging.
```

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
I used `all-MiniLM-L6-v2` via `sentence-transformers`, run locally. I chose it because it performs well on short English text — my reviews average 300–500 characters — and it's fast and free to run without any API calls.

**Production tradeoff reflection:**
The biggest issue I'd want to fix is sarcasm — reviews like "Hate is a strong word, but..." can fool MiniLM into treating them as neutral. A bigger model like `bge-large-en-v1.5` would handle that better. I'd also add BM25 keyword search alongside the vectors, since students search by exact terms like "CSC 540" or a professor's last name that pure vector search sometimes misses. Context length and multilingual support aren't concerns here — all reviews are short and in English.

---

## Retrieval test results 


```
============================================================
Query: Who is a better professor for CSC 326 — Sarah Heckman or John-Paul Ore?
  [1] dist=0.3547 | RMP_Sarah_Heckman.txt #14 | prof=Sarah Heckman course=CSC 216
      Dr. Heckman is one of the best professors I've had so far in CSC. She is very approachable and knowledgeable. It's clear...
  [2] dist=0.4357 | RMP_Sarah_Heckman.txt #17 | prof=Sarah Heckman course=CSC 230
      Dr. Heckman is a fantastic instructor. You can tell she really has a passion for what she teaches, because whenever she ...
  [3] dist=0.4753 | RMP_JohnPaul_Ore.txt #2 | prof=John-Paul Ore course=CSC 326
      Dr. Ore is one of the few gems in CSC. Dr. Ore genuinely cares for his students. Quizzes are easy, and labs are manageab...
  [4] dist=0.4786 | RMP_Sarah_Heckman.txt #6 | prof=Sarah Heckman course=CSC 216
      Dr. Heckman is a good lecturer but she moves really fast. However, the class is really just hard. There's project milest...
  [5] dist=0.4873 | RMP_Sarah_Heckman.txt #9 | prof=Sarah Heckman course=CSC 216
      Dr. Heckman was very knowledgeable and a great lecturer. She went over notes and information in lectures and gave us tip...
```

Results [1], [2], [4], [5] are Heckman reviews — relevant because her name is in the query. However, all four are from CSC 216 and CSC 230, not CSC 326. Only result [3] is actually about Ore in CSC 326, which is what the query is asking about. This is the retrieval bias problem: Heckman has more reviews overall so her chunks dominate, and the model doesn't have enough CSC 326-specific context for both professors to make a fair comparison.

```
============================================================
Query: How is Professor Kemafor Ogan?
  [1] dist=0.4068 | RMP_Kemafor_Ogan.txt #13 | prof=Kemafor Anyanwu Ogan course=CSC 540
      Professor Kemafor is often underprepared for her classes as we can see her get confused all the time. The concepts that ...
  [2] dist=0.4923 | RMP_Kemafor_Ogan.txt #2 | prof=Kemafor Anyanwu Ogan course=CSC 540
      Many students take Prof. Kemafor's class only to fulfill credit requirements, not because she's a great professor. She l...
  [3] dist=0.4980 | RMP_Kemafor_Ogan.txt #11 | prof=Kemafor Anyanwu Ogan course=CSC 540
      Dr. Ogan and her TAs are absolutely awful. Dr. Ogan seemed to be underprepared for her classes and did not follow her lo...
  [4] dist=0.4985 | RMP_Kemafor_Ogan.txt #17 | prof=Kemafor Anyanwu Ogan course=CSC 540
      Dr. Ogan was the worst professor that I had at NCSU. I highly discourage from taking any course with her. She forgets wh...
  [5] dist=0.5510 | RMP_Kemafor_Ogan.txt #12 | prof=Kemafor Anyanwu Ogan course=CSC 541
```

All 5 results are Ogan reviews — exactly right. The query mentions her name directly, so the embedding similarity is high across all her reviews. Distances are tight (0.40–0.55), meaning the model is confident these are the most relevant chunks. This query worked cleanly.

```
============================================================
Query: pineapple pizza
  [1] dist=0.7800 | RMP_JohnPaul_Ore.txt #6 | prof=John-Paul Ore course=CSC 326
      Gave us donuts and was very nice to all students. Very enthusiastic in all lectures. Known to some as GOAT-Paul Ore for ...
  [2] dist=0.7970 | RMP_JohnPaul_Ore.txt #5 | prof=John-Paul Ore course=CSC 326
      Professor GOAT-Paul Ore is the professor that you have to take for Software Engineering. He is extremely energetic and k...
  [3] dist=0.8696 | RMP_JohnPaul_Ore.txt #4 | prof=John-Paul Ore course=CSC 326
      His lectures were entertaining and informative and it was easy to tell that he cared about the students. He was very app...
  [4] dist=0.8834 | CSC_520.txt #2 | prof= course=CSC 520
      Her accent is Iranian, I think...
  [5] dist=0.8901 | CSC_116.txt #17 | prof= course=CSC 116
      Unlike high school, you don't get to skim through CSC 116 by having a basic understanding of coding logic. You need to r...
```

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
I used the following system prompt to enforce grounding: "Answer the user's question using ONLY the student reviews provided in the REVIEWS CONTEXT block of the user message. Treat that text as your single source of truth. Do NOT use any outside or prior knowledge about professors, courses, or NCSU, even if you are confident you know the answer. Do NOT infer, assume, or fill in details that are not explicitly stated in the provided reviews." I also defined a `FALLBACK_MESSAGE` constant with the exact text the model must return word-for-word when the reviews don't cover the question — this prevents the model from generating a plausible-sounding answer from its training data instead of admitting it doesn't know.

**How source attribution is surfaced in the response:**
I structured each retrieved chunk in the user message with a header in the format `[RMP_Sarah_Heckman.txt | prof=Sarah Heckman | course=CSC 216]` so the filename is visible to the model. The system prompt then instructs it to cite the filename inline immediately after any claim, using the format `(source: RMP_Sarah_Heckman.txt)`. I also programmatically collect the source filenames from the retrieved chunks in `generate_answer()` and return them as a separate `sources` list, which the Gradio UI displays in a dedicated "Retrieved from" box — so attribution is guaranteed structurally, not left entirely up to the LLM.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Who's a better professor for CSC 326 — Sarah Heckman or John-Paul Ore? | John-Paul Ore. All his CSC 326 reviews are 5-star; students call him "GOAT-Paul Ore" and praise his energy and care. Heckman's CSC 326 reviews are mixed-to-negative (quality 1–3): lectures don't connect to labs, she can be dismissive, and she over-emphasizes process over engineering. | I couldn't find an answer to that in the loaded reviews. I can only answer from the student reviews I have for these NCSU CS professors and courses: Sarah Heckman, John-Paul Ore, Kemafor Ogan, Thomas Price, Vincent Freeh, CSC 116, CSC 216, CSC 226, CSC 326, and CSC 520. Try rephrasing your question, or make sure you're asking about one of those. | Off-target | Inaccurate |
| 2 | How is Professor Kemafor Ogan? | Overwhelmingly negative — nearly all reviews give quality 1. Recurring complaints: disorganized and unprepared, unclear project specs, exam questions harder than what's taught, and arbitrary grading. One outlier (CSC 454) is positive, but students across CSC 440, 540, and 541 consistently say to avoid her. | Professor Kemafor Ogan is often described as being underprepared for her classes, lacking teaching skills, and having difficulty explaining concepts clearly (source: RMP_Kemafor_Ogan.txt). Many students have expressed disappointment with her teaching style, citing that her classes are tedious to listen to and that the questions on exams are of a higher level of difficulty than what is taught in class (source: RMP_Kemafor_Ogan.txt). Some students have also reported that she lacks professionalism, citing an incident where she allegedly asked a student for a picture of their medicine bottle and purchase receipt, which was seen as a privacy violation (source: RMP_Kemafor_Ogan.txt). Additionally, her project documents and assignments have been described as confusing and unclear, with some students receiving feedback and grades late in the semester (source: RMP_Kemafor_Ogan.txt). Overall, the reviews suggest that Professor Kemafor Ogan is not well-regarded by her students, with one reviewer stating that she was the worst professor they had at NCSU (source: RMP_Kemafor_Ogan.txt). | Relevant | Accurate |
| 3 | How is CSC 216 with professor Sarah Heckman? | Mostly positive — knowledgeable, passionate, detailed slides — but time-intensive. Projects take longer than estimated (start Part 2 early), the final has heavy code-writing by hand, and there is a minimum grade requirement. Worth it if you stay on top of deadlines. | According to student reviews of Sarah Heckman (source: RMP_Sarah_Heckman.txt), Dr. Heckman is one of the best professors for CSC 216, being very approachable and knowledgeable, and it's clear she wants students to understand how to write good code for industry. Students are advised to start on the projects early and study lots for the tests, as the final has lots of code writing on it (source: RMP_Sarah_Heckman.txt). Another student also took her class for CSC 216 and recommends doing the same, indicating a positive experience (source: RMP_Sarah_Heckman.txt). | Relevant | Accurate |
| 4 | Tips for CSC 116 with Dr. Schmidt? | Read the full textbook (videos are just summaries), do Practice It problems, and start projects the day they are released — Project 4 is especially time-consuming. Design your algorithm on paper before coding. Schmidt is harder than Balik but prepares you better for CSC 216. | Based on the reviews, it seems that Dr. Schmidt is a good option for CSC 116, especially if you want to be well-prepared for CSC 216 (source: CSC_116.txt). One tip is that she goes over the foundations well, which can set you up for success in future courses (source: CSC_116.txt). However, it's also mentioned that if you have little programming experience, you might want to avoid her, as the class may be challenging (source: CSC_116.txt). Additionally, be prepared for a decent amount of work in the class (source: CSC_116.txt). | Relevant | Accurate |
| 5 | Are Heckman's exams hard? | Mixed. Some say exams are fair with partial credit and that her detailed slides make studying easy. Others say they're harder than expected, especially the final which requires writing a lot of code by hand. Manageable if you attend lectures and study her slides, but the final can surprise you. | According to some student reviews of Sarah Heckman's CSC 216 class (source: RMP_Sarah_Heckman.txt), the exams are considered hard, with one review stating that "The exams are more difficult than they should be, especially the final" and another review mentioning that the class is "really just hard" with exams and project deadlines coinciding. However, another review of the same class (source: RMP_Sarah_Heckman.txt) describes the exams as "relatively easy" with "lots of partial credit", presenting a conflicting view. In her CSC 326 class (source: RMP_Sarah_Heckman.txt), the midterm and final exams are described as constituting a relatively small portion of the grade, but their difficulty is not commented on. | Relevant | Accurate |

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
Who's a better professor for CSC 326 — Sarah Heckman or John-Paul Ore?

**What the system returned:**
I couldn't find an answer to that in the loaded reviews. I can only answer from the student reviews I have for these NCSU CS professors and courses: Sarah Heckman, John-Paul Ore, Kemafor Ogan, Thomas Price, Vincent Freeh, CSC 116, CSC 216, CSC 226, CSC 326, and CSC 520. Try rephrasing your question, or make sure you're asking about one of those.

**Root cause (tied to a specific pipeline stage):**
I expected this answer to go wrong due to model bias based on retrieval of more answers for one professor over the other, which is still happening in retrieval stage. We have top_k = 5, so the retrieval is returning 4 Heckman reviews and only 1 Ore review. The LLM is determining that it can't make a CSC 326 specific comparison because of this and is triggering the fallback response. It's possible that the system prompt's grounding instruction is also too tight, and doesn't really explain this case.

**What you would change to fix it:**
I would increase `TOP_K` in `config.py` from 5 to 8–10 so that comparison queries have room to surface reviews from both professors. A more robust fix would be a pre-retrieval step that detects when a query names two professors, runs two separate filtered retrievals (one per professor), and merges the results before passing to the LLM — guaranteeing balanced context regardless of embedding similarity scores.

---

## Example Responses

**Response 1 — "How is Professor Kemafor Ogan?"**

> Professor Kemafor Ogan is often described as being underprepared for her classes, lacking teaching skills, and having difficulty explaining concepts clearly (source: RMP_Kemafor_Ogan.txt). Many students have expressed disappointment with her teaching style, citing that her classes are tedious to listen to and that the questions on exams are of a higher level of difficulty than what is taught in class (source: RMP_Kemafor_Ogan.txt). Some students have also reported that she lacks professionalism, citing an incident where she allegedly asked a student for a picture of their medicine bottle and purchase receipt, which was seen as a privacy violation (source: RMP_Kemafor_Ogan.txt). Additionally, her project documents and assignments have been described as confusing and unclear, with some students receiving feedback and grades late in the semester (source: RMP_Kemafor_Ogan.txt). Overall, the reviews suggest that Professor Kemafor Ogan is not well-regarded by her students, with one reviewer stating that she was the worst professor they had at NCSU (source: RMP_Kemafor_Ogan.txt).

*Retrieved from: RMP_Kemafor_Ogan.txt*

---

**Response 2 — "Are Heckman's exams hard?"**

> According to some student reviews of Sarah Heckman's CSC 216 class (source: RMP_Sarah_Heckman.txt), the exams are considered hard, with one review stating that "The exams are more difficult than they should be, especially the final" and another review mentioning that the class is "really just hard" with exams and project deadlines coinciding. However, another review of the same class (source: RMP_Sarah_Heckman.txt) describes the exams as "relatively easy" with "lots of partial credit", presenting a conflicting view. In her CSC 326 class (source: RMP_Sarah_Heckman.txt), the midterm and final exams are described as constituting a relatively small portion of the grade, but their difficulty is not commented on.

*Retrieved from: RMP_Sarah_Heckman.txt*

---

**Response 3 — Out-of-scope query: "What do students think of CSC 999?"**

> I couldn't find an answer to that in the loaded reviews. I can only answer from the student reviews I have for these NCSU CS professors and courses: Sarah Heckman, John-Paul Ore, Kemafor Ogan, Thomas Price, Vincent Freeh, CSC 116, CSC 216, CSC 226, CSC 326, and CSC 520. Try rephrasing your question, or make sure you're asking about one of those.

The system returned the exact `FALLBACK_MESSAGE` and did not attempt to generate a made-up answer. This confirms grounding is working — when no relevant reviews exist, the model refuses rather than hallucinating.

---

## Query Interface

The interface is a Gradio web app that runs at `http://localhost:7860` when you run `python app.py`.

**Input field:** A single text box labelled "Your question." You type a natural language question about any NCSU CS professor or course and press the "Ask" button or hit Enter.

**Output fields:**
- **Answer** — the LLM's grounded response with inline `(source: filename.txt)` citations after each claim
- **Retrieved from** — a list of the source files that were pulled from ChromaDB for that query

**Sample interaction transcript:**

```
User: Tips for CSC 116 with Dr. Schmidt?

Answer:
Based on student reviews, here are some tips for CSC 116 with Dr. Schmidt:

Dr. Schmidt goes over the foundations well and if you do well in her class, you're set
up very well for CSC 216 (source: CSC_116.txt). However, if you have little programming
experience, you might want to be cautious as the class can be challenging (source: CSC_116.txt).

Here are some specific tips:
- Read the textbook thoroughly — exams require full knowledge of Java principles and her
  videos are essentially just summaries of the textbook reading (source: CSC_116.txt).
- Do as many Practice It problems as possible for tested material (source: CSC_116.txt).
- Start projects as soon as they are released. Project 4 is the most time-consuming, so
  don't procrastinate (source: CSC_116.txt).
- For labs, figure out the algorithm and design first before programming (source: CSC_116.txt).

Retrieved from:
• CSC_116.txt
```

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
Usually, I have always worked with having an architecture design, and then implemented the project in stages. But having a detailed spec helped me keep in track about how each stage can be implemented in a more closed detail. I was able to use the spec in `planning.md` to prompt Claude to implement the files like `ingest.py`, `app.py`, `retriever.py`, `generator.py` . This was overall very helpful in a quicker coding with Claude Code. I think if I had to develop this on my own, I'd need much more time.

**One way your implementation diverged from the spec, and why:**
While building `generator.py` I ended up not using the `filters` parameter in `retrieve()` function even though I had added it to the planning.md file. The reason being, this was getting to tightly coupled and was adding complexity which might not even work. In a scenario where the question might use a nickname of the professor or the course is worded differently the filters we have set wouldn't work out. 

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1 — Implementing `ingest.py`**

I gave Claude the Chunking Strategy section from `planning.md` and two sample files (`RMP_JohnPaul_Ore.txt` and `CSC_116.txt`) so it could see both the RMP review format and Reddit comment format. I asked it to write `load_documents()` and `chunk_documents()`.

Claude produced both functions — `load_documents()` using `pathlib.glob`, `chunk_documents()` splitting on `=== REVIEW N ===` / `=== COMMENT N ===` with regex, and a metadata parser that returns `None` for missing fields. It also included a smoke-test that verified chunk counts.

I then directed it to replace `pathlib` with `os.listdir(DOCS_PATH)` importing from `config.py`, and changed the smoke-test to print 5 random chunks with full text and character count instead of just the first 3.

**Instance 2 — Building `retriever.py` and fixing distance scores**

I gave Claude the Retrieval Approach section from `planning.md` and the chunk format from `ingest.py`, and asked it to implement `embed_and_store()` and `retrieve()` using `sentence-transformers` and ChromaDB.

Claude produced both functions with a smoke-test covering 5 queries, a metadata filter check, and a nonsense query.

After running it, I noticed the distance scores looked high (0.7–1.1) against a warning that "scores above 0.6–0.7 indicate weak matches." I asked Claude to investigate. It found that ChromaDB defaults to L2 distance (range 0–2) instead of cosine distance (range 0–1), which was inflating the numbers. I overrode the collection to use `{"hnsw:space": "cosine"}`, deleted and re-embedded, and scores dropped to 0.27–0.55 for strong matches.
