import os
import re
import random

from config import DOCS_PATH

_KNOWN_REVIEW_KEYS = {"course", "date", "quality", "difficulty", "grade", "would_take_again", "tags"}


def load_documents():
    """Read every .txt file in DOCS_PATH and return a list of (source_file, raw_text, file_metadata) tuples."""
    docs = []
    for filename in sorted(os.listdir(DOCS_PATH)):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(DOCS_PATH, filename)
        with open(filepath, encoding="utf-8") as f:
            raw = f.read()
        file_meta = _parse_file_header(raw)
        file_meta["source_file"] = filename
        docs.append((filename, raw, file_meta))

    print(f"[load_documents] Loaded {len(docs)} documents.")
    for source_file, raw_text, file_meta in docs:
        print(f"  {source_file} | professor={file_meta.get('professor_name')} | course={file_meta.get('course')} | chars={len(raw_text)}")

    return docs


def chunk_documents(docs=None):
    """Split each document into chunks — one per review/comment block.

    Returns a list of dicts with keys:
        text     – review body only (metadata lines stripped)
        metadata – structured fields: professor_name, course_name, quality,
                   difficulty, grade, would_take_again, tags, date, source_file,
                   chunk_index, chunk_type
    Missing optional fields are None rather than absent.
    """
    if docs is None:
        docs = load_documents()

    chunks = []
    for source_file, raw_text, file_meta in docs:
        review_blocks = re.findall(
            r"=== REVIEW (\d+) ===\n(.*?)=== END REVIEW \1 ===",
            raw_text,
            re.DOTALL,
        )
        comment_blocks = re.findall(
            r"=== COMMENT (\d+) ===\n(.*?)=== END COMMENT \1 ===",
            raw_text,
            re.DOTALL,
        )

        if review_blocks:
            professor_name = file_meta.get("professor_name")
            for n, block in review_blocks:
                chunk = _parse_review_block(block, int(n), professor_name, source_file, file_meta)
                if chunk:
                    chunks.append(chunk)
        elif comment_blocks:
            course_name = _normalize_course_name(file_meta.get("course", ""))
            for n, block in comment_blocks:
                text = block.strip()
                if not text:
                    continue
                chunks.append({
                    "text": text,
                    "metadata": {
                        "professor_name": None,
                        "course_name": course_name or None,
                        "quality": None,
                        "difficulty": None,
                        "grade": None,
                        "would_take_again": None,
                        "tags": None,
                        "date": None,
                        "source_file": source_file,
                        "chunk_index": int(n),
                        "chunk_type": "comment",
                    },
                })

    return chunks


# ── helpers ──────────────────────────────────────────────────────────────────


def _parse_file_header(raw_text):
    """Return a dict of key/value pairs from the --- DOCUMENT METADATA --- block."""
    metadata = {}
    match = re.search(
        r"--- DOCUMENT METADATA ---\n(.*?)\n--- END METADATA ---",
        raw_text,
        re.DOTALL,
    )
    if not match:
        return metadata
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            metadata[key.strip()] = value.strip()
    return metadata


def _parse_review_block(block_content, chunk_index, professor_name, source_file, file_meta):
    """Parse one === REVIEW N === block into a chunk dict."""
    fields = {}
    body_lines = []
    in_body = False

    for line in block_content.splitlines():
        if in_body:
            body_lines.append(line)
            continue
        stripped = line.strip()
        if not stripped:
            in_body = True
            continue
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            key_norm = key.strip().lower().replace(" ", "_")
            if key_norm in _KNOWN_REVIEW_KEYS:
                fields[key_norm] = value.strip()
                continue
        # Unrecognized line after metadata block — treat as body start
        in_body = True
        body_lines.append(line)

    text = "\n".join(body_lines).strip()
    if not text:
        return None

    course_name = _normalize_course_name(
        fields.get("course") or file_meta.get("course", "")
    )

    return {
        "text": text,
        "metadata": {
            "professor_name": professor_name,
            "course_name": course_name or None,
            "quality": _to_float(fields.get("quality")),
            "difficulty": _to_float(fields.get("difficulty")),
            "grade": fields.get("grade") or None,
            "would_take_again": fields.get("would_take_again") or None,
            "tags": fields.get("tags") or None,
            "date": fields.get("date") or None,
            "source_file": source_file,
            "chunk_index": chunk_index,
            "chunk_type": "review",
        },
    }


def _normalize_course_name(raw):
    """Strip description suffix: 'CSC 116 - Introduction to Computing: Java' → 'CSC 116'."""
    if not raw:
        return raw
    return raw.split(" - ")[0].strip()


def _to_float(value):
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


# ── quick smoke-test ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    print(f"Total chunks: {len(chunks)}\n")

    for source_file, raw_text, _ in docs:
        review_count = len(re.findall(r"=== REVIEW \d+ ===", raw_text))
        comment_count = len(re.findall(r"=== COMMENT \d+ ===", raw_text))
        file_chunks = [c for c in chunks if c["metadata"]["source_file"] == source_file]
        expected = review_count or comment_count
        status = "OK" if len(file_chunks) == expected else f"MISMATCH (expected {expected})"
        print(f"{source_file}: {len(file_chunks)} chunks [{status}]")

    print("\nSpot-check (5 random chunks):")
    for chunk in random.sample(chunks, 5):
        m = chunk["metadata"]
        print(
            f"\n  [{m['source_file']} #{m['chunk_index']}] "
            f"prof={m['professor_name']} course={m['course_name']} "
            f"quality={m['quality']} grade={m['grade']}"
        )
        print(f"  size: {len(chunk['text'])} chars")
        print(f"  text:\n{chunk['text']}")