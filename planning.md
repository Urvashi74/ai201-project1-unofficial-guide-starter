# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

Chosen Domain: Student reviews and evaluations of CS Professors and courses at NC State University (NCSU).

This knowledge is valuable because official course catalogs describe *what* is taught but
never *how* — teaching style, grading transparency, exam difficulty, workload, and whether a
professor's office hours are actually useful. Students currently piece this together from scattered
Rate My Professors pages, Reddit threads, and word-of-mouth, with no single searchable source. This would save prospective students hours of research and help them figure out their queries quickly. 

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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
| 10 | Reddit Thread - CSC 520 | Student Discussion | https://www.reddit.com/r/NCSU/comments/k38f2u/csc_520ai_1_with_dr_bita_akram/, https://www.reddit.com/r/NCSU/comments/k9xc41/has_anyone_taken_csc_520_artificial_intelligence/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 
One review per chunk (variable size, ~150–1500 characters). No fixed character cap — chunks are bounded by the `=== REVIEW N ===` / `=== COMMENT N ===` delimiters already present in each source file.

**Overlap:** 
None (0 characters). Each review is a self-contained semantic unit, so there is no cross-chunk continuity to preserve.

**Reasoning:**

**Strategy: semantic (delimiter-based) chunking.** Every document in `documents/` is already structured as a sequence of discrete review/comment blocks with explicit markers (`=== REVIEW N ===` for RMP files, `=== COMMENT N ===` for Reddit threads). Each block is one student's opinion — the natural unit of retrieval. Splitting on these markers gives us one opinion per chunk, which produces clean embedding signal (one sentiment, one topic, one professor/course per vector).

**Why no overlap:** Overlap exists to preserve context across arbitrary cut points. Our cuts aren't arbitrary — they fall on review boundaries, and each review is self-contained. The only context that *would* need to flow across chunks (which professor / course this review is about) is handled by structured metadata, not text overlap.

**Metadata per chunk:** Each chunk carries structured fields parsed from both the file-level header and the per-review block: `professor_name`, `course_name`, `quality`, `difficulty`, `grade`, `would_take_again`, `tags`, `date`, `source_file`. This enables hybrid filter + semantic retrieval (e.g., filter by `professor_name=Heckman AND course_name=CSC 216`, then semantic-rank within that subset). The chunk text itself is the review body only — numeric metadata is stripped from the embedded text to reduce noise, but tags are kept in or prepended to the text since they carry semantic signal.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
Embedding model chosen: all-MiniLM-L6-v2 (via sentence-transformers)
It's strong on short English text, the doc reviews have average of ~300-500 characters. 

**Top-k:**
Setting top_k = 5
Chunks are pretty small, one chunk has one opinion/review. 5 opinions are a good average to generate context about a course or professor.

**Production tradeoff reflection:**

* Better understanding of tone and sarcasm. Reviews are full of sarcasm and strong emotion ("Hate is a strong word, but..."). A bigger model like OpenAI's text-embedding-3-large or bge-large-en-v1.5 would catch that nuance better than MiniLM, which can read sarcastic praise as actual praise.
* Exact keyword matches. Students search by exact terms like "CSC 540" or a professor's last name. Pure vector search sometimes misses those. I'd add BM25 (keyword search) alongside the embeddings and combine the scores — this usually helps more than upgrading the embedding model.
* A re-ranker for better top results. Use a cheap model to grab the top 50 chunks, then a stronger cross-encoder (like ms-marco-MiniLM-L-12-v2) to re-rank them down to the top 5. Usually a bigger quality win than swapping the embedder.
* Context length isn't really a concern. Reviews are short — even the longest ones fit easily in any modern embedding model.
* Multilingual support isn't needed. All reviews are in English.
* Latency doesn't matter at this scale. With ~100 chunks, any model is fast enough. It would only matter if I expanded to every NCSU professor and course (thousands of reviews).
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Who's a better professor for CSC 326 — Sarah Heckman or John-Paul Ore? |  John-Paul Ore.. (followed by review summary of how he has a glowing review) |
| 2 | How is Professor Kemafor Ogan? | Overall negative review reflected through all the complaints students have in their reviews. |
| 3 | How is CSC 216 with professor Sarah Heckman? | Pretty positive, with some mixed answers since projects can be harder. |
| 4 | Tips for CSC 116 with Dr. Schmidt? | Read the textbook, start projects the day they are released. |
| 5 | Are Heckman's exams hard? | Mixed reviews. Some say its fair, others say its hard. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic retrieval, chunks that split key information across boundaries. -->

1. Comparison Queries could return biased answers.
With k=5, might get more responses of one side, creating bias towards the one. For example, "Heckman or Ore" - if we get 4 for Ore, and 1 for Heckman review or vice-versa, then the comparison can bias towards whicever professor has more tectually similar reviews.

2. Sarcasm and emotional language, could confuse the embedding model.
Reviews are full of sarcasm, exaggeration, and slang that doesn't always match the literal sentiment of the words. MiniLM-L6-v2 will sometimes match sarcastic praise to "good professor" queries and miss emotional negative reviews that don't use obvious negative keywords.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
+--------------------------------------------------------------------+
|  STAGE 1: DOCUMENT INGESTION                                       |
|  --------------------------------------------------------------    |
|  - Read .txt files from documents/                                 |
|  - Parse file-level metadata header                                |
|      (professor_name OR course_name)                               |
|  Tool: Python  (pathlib, open)                                     |
+--------------------------------------------------------------------+
                                |
                                v
+--------------------------------------------------------------------+
|  STAGE 2: CHUNKING                                                 |
|  --------------------------------------------------------------    |
|  - Semantic / delimiter-based split on                             |
|      === REVIEW N ===  (RMP files)                                 |
|      === COMMENT N === (Reddit threads)                            |
|  - One review = one chunk, NO overlap                              |
|  - Parse per-review metadata into structured fields                |
|      (course, quality, difficulty, grade, tags, date)              |
|  Tool: Python  (re module)                                         |
+--------------------------------------------------------------------+
                                |
                                v
+--------------------------------------------------------------------+
|  STAGE 3: EMBEDDING + VECTOR STORE                                 |
|  --------------------------------------------------------------    |
|  - Embed chunk body text (384-dim vectors)                         |
|  - Store vectors + structured metadata                             |
|  Embedding model: all-MiniLM-L6-v2                                 |
|  Library:         sentence-transformers                            |
|  Vector store:    ChromaDB (local, persistent)                     |
+--------------------------------------------------------------------+
                                |
                                v
+--------------------------------------------------------------------+
|  STAGE 4: RETRIEVAL                                                |
|  --------------------------------------------------------------    |
|  user query                                                        |
|     |                                                              |
|     +--> embed with all-MiniLM-L6-v2                               |
|     +--> optional metadata pre-filter                              |
|             (professor_name / course_name / quality)               |
|     +--> semantic similarity search, top_k = 5                     |
|  Tool: ChromaDB .query() with where={...} filter                   |
+--------------------------------------------------------------------+
                                |
                                v
+--------------------------------------------------------------------+
|  STAGE 5: GENERATION                                               |
|  --------------------------------------------------------------    |
|  - Prompt: question + top-5 chunks (with metadata)                 |
|  - LLM produces grounded answer that cites source reviews          |
|  Model:   llama-3.3-70b-versatile  (free tier, OpenAI-compatible)  |
|  Client:  from groq import Groq                                    |
+--------------------------------------------------------------------+
                                |
                                v
                       answer to student
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
AI Tool used: Claude
Input:
- The "Documents" and "Chunking Strategy" sections of this planning.md
- Two sample files from `documents/` (e.g., `RMP_Sarah_Heckman.txt`, `CSC_226.txt`) so Claude sees the actual format
- Instruction: create a file ingest.py, write `load_documents()` that reads every `.txt` file in `documents/` and parses the file-level metadata header (professor_name OR course_name), and `chunk_documents()` that splits on `=== REVIEW N ===` / `=== COMMENT N ===` and parses each per-review metadata block into structured fields.

Expected output:
- Two Python functions that return a list of chunk objects of the form `{text, metadata}`, where metadata includes `professor_name`, `course_name`, `quality`, `difficulty`, `grade`, `would_take_again`, `tags`, `date`, `source_file`.

Verification:
- Run on one file and check the number of chunks equals the number of `=== REVIEW N ===` blocks.
- Spot-check 2–3 chunks: chunk text should be only the review body (no metadata lines), and metadata fields should be filled correctly.
- Confirm reviews missing optional fields (e.g., no `grade`) return `None` instead of crashing.

**Milestone 4 — Embedding and retrieval:**
AI Tool used: Claude
Input:
- The "Retrieval Approach" section of this planning.md
- The chunk object format from Milestone 3
- Instruction: write `embed_and_store()` that embeds each chunk's text with `all-MiniLM-L6-v2` (via `sentence-transformers`) and stores it in a local ChromaDB collection with its metadata. Then write `retrieve(query, filters=None, top_k=5)` that embeds the query, applies an optional metadata `where` filter, and returns the top-5 most similar chunks.

Expected output:
- A persistent ChromaDB collection on disk with every chunk embedded.
- A retrieval function returning the top-5 ranked chunks with text + metadata.

Verification:
- Run a known-answer query like "Sarah Heckman CSC 216" and confirm at least 3 of the top 5 are Heckman CSC 216 reviews.
- Test metadata filtering: `retrieve("good professor", filters={"professor_name": "John-Paul Ore"})` should return only Ore reviews.
- Try a nonsense query ("pineapple pizza") and confirm the system still returns 5 results without crashing.

**Milestone 5 — Generation and interface:**
AI Tool used: Claude
Input:
- The "Architecture" section of this planning.md (shows the Stage 5 model + client)
- The `retrieve()` function from Milestone 4
- Instruction: write `generate_answer(question)` that calls `retrieve()` to get the top-5 chunks, builds a prompt with the question + retrieved review text and metadata, and sends it to Groq using `from groq import Groq` with model `llama-3.3-70b-versatile`. The system prompt must tell the model to answer using ONLY the retrieved reviews and to cite source review IDs. Wrap it in a simple CLI loop so the user can type a question and see the answer.

Expected output:
- A working CLI: user types a question → system retrieves chunks → LLM produces a grounded answer with source citations.

Verification:
- Run all 5 evaluation questions from the Evaluation Plan section and check each answer matches the expected answer.
- Confirm the answer cites specific reviews (so it's grounded, not hallucinated).
- Ask a question about a topic not in the docs (e.g., "What do students say about CSC 999?") and confirm the model says it doesn't know instead of making something up.