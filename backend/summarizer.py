# backend/summarizer.py
import os
import math
import time
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("doc_summarizer")

# Optional: import Groq SDK; ensure it's in requirements.txt
try:
    from groq import Groq
except Exception:
    Groq = None

GROQ_API_KEY = os.getenv("GROQ_API_KEY", None)
if Groq and GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None

# Tunable limits (chars approximate — tokens vs chars varies by language/model)
CHUNK_MAX_CHARS = 9000   # each chunk will be roughly up to this many characters
COMBINE_SUMMARIES_THRESHOLD = 16000  # if combined summaries still long, we re-summarize

def _call_groq(prompt, model="llama-3.1-8b-instant", timeout=60):
    """
    Call Groq chat completions safely and return text.
    This function handles either dict-style or object-style responses.
    """
    if client is None:
        raise RuntimeError("Groq client not configured. Set GROQ_API_KEY in env.")

    # Build messages payload
    messages = [{"role": "user", "content": prompt}]
    # attempt the call with error handling
    try:
        response = client.chat.completions.create(model=model, messages=messages, timeout=timeout)
        # response.choices[0].message might be an object or dict
        choice = getattr(response, "choices", None)
        if not choice:
            # try as dict
            if isinstance(response, dict) and "choices" in response:
                choice0 = response["choices"][0]
                msg = choice0.get("message") or choice0.get("text") or choice0
                if isinstance(msg, dict):
                    return msg.get("content") or msg.get("text") or str(msg)
                else:
                    return getattr(msg, "content", None) or getattr(msg, "text", None) or str(msg)
            raise RuntimeError("Unexpected Groq response shape")
        # choice may be a list-like
        c0 = response.choices[0]
        # message might be attribute or dict
        msg = getattr(c0, "message", None) or (c0.get("message") if isinstance(c0, dict) else None)
        if isinstance(msg, dict):
            return msg.get("content") or msg.get("text") or ""
        else:
            # object style
            return getattr(msg, "content", None) or getattr(msg, "text", None) or str(msg)
    except Exception as e:
        logger.exception("Groq API error")
        raise

def _summarize_single_chunk(chunk_text, length):
    """
    Single-call summarization prompt for a chunk.
    length: 'short'|'medium'|'long'
    """
    length_map = {
        "short": "Summarize concisely in 3–4 sentences, focusing on the most important points.",
        "medium": "Summarize in a medium-length paragraph (6–10 sentences), covering key points.",
        "long": "Summarize in detail, covering all major points clearly and thoroughly."
    }
    instruction = length_map.get(length, length_map["medium"])
    prompt = f"You are an expert document summarizer.\n{instruction}\n\nDocument:\n{chunk_text}\n\nProvide the summary, keep it in plain text (no Markdown or extra symbols)."
    return _call_groq(prompt)

def generate_summary(full_text, length="medium"):
    """
    High-level function used by backend. It will:
     - If text is small: call model once
     - If large: split into chunks, summarize each, then combine & final-summarize
    """
    if not full_text or not full_text.strip():
        return ""

    # If small, call directly
    if len(full_text) <= CHUNK_MAX_CHARS:
        return _summarize_single_chunk(full_text, length).strip()

    # Otherwise, chunk
    chunks = []
    text = full_text.strip()
    start = 0
    L = len(text)
    while start < L:
        end = min(start + CHUNK_MAX_CHARS, L)
        # try to cut on newline/space for nicer splits
        if end < L:
            # look back for newline or space
            cut = text.rfind("\n", start, end)
            if cut <= start:
                cut = text.rfind(" ", start, end)
            if cut > start:
                end = cut
        chunks.append(text[start:end].strip())
        start = end

    # Summarize each chunk
    chunk_summaries = []
    for idx, c in enumerate(chunks):
        try:
            s = _summarize_single_chunk(c, length)
            chunk_summaries.append(s.strip())
            # small sleep to avoid bursting rate limits (optional)
            time.sleep(0.2)
        except Exception as e:
            logger.exception("Error summarizing chunk %d", idx)
            raise RuntimeError(f"Error summarizing chunk {idx}: {e}")

    # Combine summaries
    combined = "\n\n".join(chunk_summaries)
    # If combined is still big, shorten it first
    if len(combined) > COMBINE_SUMMARIES_THRESHOLD:
        # ask model to compress combined summaries into a coherent summary
        try:
            combined = _summarize_single_chunk(combined, "long")
        except Exception as e:
            logger.exception("Error compressing combined summaries")
            raise

    # Final polish/lengthing step: respect requested length
    final_summary = _summarize_single_chunk(combined, length)
    return final_summary.strip()
