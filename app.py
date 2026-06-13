import gradio as gr

from ingest import load_documents, chunk_documents
from retriever import embed_and_store, _get_collection
from generator import generate_answer
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

def startup():
    """Run ingestion, chunking, and embedding (skips embedding if store already populated)."""
    print("[app] Stage 1 & 2 — Loading and chunking documents...")
    docs = load_documents()
    chunks = chunk_documents(docs)

    print("[app] Stage 3 — Checking vector store...")
    collection = _get_collection()
    if collection.count() == 0:
        print("[app] No embeddings found — running embed_and_store()...")
        embed_and_store(chunks)
    else:
        print(f"[app] Vector store already has {collection.count()} chunks — skipping re-embedding.")

    print("[app] Pipeline ready.\n")


def handle_query(question):
    if not question.strip():
        return "", ""
    result = generate_answer(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


startup()

with gr.Blocks(title="NCSU CS Unofficial Guide") as demo:
    gr.Markdown(
        "## NCSU CS Unofficial Guide\n"
        "Ask anything about CS professors and courses at NC State — "
        "answers are grounded in real student reviews."
    )
    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. How is Professor Heckman for CSC 216?",
    )
    btn = gr.Button("Ask", variant="primary")
    answer_box = gr.Textbox(label="Answer", lines=8)
    sources_box = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer_box, sources_box])
    inp.submit(handle_query, inputs=inp, outputs=[answer_box, sources_box])

demo.launch(server_port=7860)
