from groq import Groq

from config import GROQ_API_KEY, LLM_MODEL
from retriever import retrieve

_client = None

FALLBACK_MESSAGE = (
    "I couldn't find an answer to that in the loaded reviews. I can only answer "
    "from the student reviews I have for these NCSU CS professors and courses: "
    "Sarah Heckman, John-Paul Ore, Kemafor Ogan, Thomas Price, Vincent Freeh, "
    "CSC 116, CSC 216, CSC 226, CSC 326, and CSC 520. "
    "Try rephrasing your question, or make sure you're asking about one of those."
)

# Static system prompt — grounding rules, citation format, and fallback behaviour.
# Contains no review text and no user question; those go in the user message,
# so this stays identical on every call.
SYSTEM_PROMPT = (
    "You are NCStateGuide, a student-review assistant for NC State University CS courses. "
    "Answer the user's question using ONLY the student reviews provided in the "
    "REVIEWS CONTEXT block of the user message. Treat that text as your single source of truth.\n\n"
    "- Do NOT use any outside or prior knowledge about professors, courses, or NCSU, "
    "even if you are confident you know the answer.\n"
    "- Do NOT infer, assume, or fill in details that are not explicitly stated "
    "in the provided reviews.\n"
    "- If the reviews do not contain enough information to meaningfully address "
    "the question, reply with exactly the following message and nothing else:\n"
    f'    "{FALLBACK_MESSAGE}"\n\n'
    "When you can answer, cite the source file inline using the format "
    "(source: <filename>) immediately after any claim you make — for example: "
    "'According to student reviews of Sarah Heckman (source: RMP_Sarah_Heckman.txt), "
    "exams focus heavily on code writing by hand.' "
    "Use only the filename shown in the [<filename> | ...] header of the review "
    "you relied on. Do not invent or guess filenames. If relevant sources span "
    "more than one file, cite each file alongside the part of the answer it supports.\n\n"
    "A correct \"that isn't in the loaded reviews\" is always better than a "
    "confident answer drawn from outside the provided text."
)


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def generate_answer(question):
    """Retrieve top-k chunks and generate a grounded answer via Groq.

    Returns:
        dict with keys:
            answer  – LLM response grounded in retrieved reviews
            sources – list of source_file strings cited
    """
    chunks = retrieve(question)

    # Build numbered context block; label carries professor/course so the LLM
    # can name the source in its answer without guessing.
    context_lines = []
    for chunk in chunks:
        m = chunk["metadata"]
        header = f"[{m['source_file']} | prof={m['professor_name'] or 'N/A'} | course={m['course_name'] or 'N/A'}]"
        context_lines.append(f"{header}\n{chunk['text']}")
    context = "\n\n".join(context_lines)

    user_prompt = f"REVIEWS CONTEXT:\n{context}\n\nQuestion: {question}"

    response = _get_client().chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    answer = response.choices[0].message.content
    sources = list(dict.fromkeys(c["metadata"]["source_file"] for c in chunks))

    return {"answer": answer, "sources": sources}
