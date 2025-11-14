from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -------------------------------
# Split PDF text safely into chunks
# -------------------------------
def split_into_chunks(text, max_chars=3500):
    chunks = []
    while len(text) > max_chars:
        part = text[:max_chars]

        # Try to end at a sentence boundary
        boundary = part.rfind(". ")
        if boundary == -1:
            boundary = max_chars

        chunks.append(text[:boundary + 1])
        text = text[boundary + 1:]

    if text.strip():
        chunks.append(text)

    return chunks


# -------------------------------
# Summarize a single chunk
# -------------------------------
def summarize_chunk(chunk, instruction):
    prompt = f"""
You are an expert summarizer.

Follow these formatting rules VERY STRICTLY:

1. The summary must be written as clean, continuous text.
2. Do NOT use any bullet points.
3. Do NOT use *, -, +, •, or any list symbols.
4. Do NOT format lists or headings.
5. Do NOT preserve any formatting from the original text.
   - If the original document contains **bold**, remove it.
   - If the original document contains lists, remove them.
6. Only bold words or phrases that are TRULY important.
   - Maximum 3 to 7 bold highlights per summary.
7. The summary should look natural, smooth, and professional.
8. Write in one paragraph or two paragraphs (no more).

Now provide a clean, well-structured summary based on the following document. Follow the above rules exactly.


Task: {instruction}

Document chunk to summarize:
{chunk}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You produce clear, structured, highlighted summaries."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()



# -------------------------------
# Main summarizer (CHUNKED)
# -------------------------------
def generate_summary(text, length="medium"):
    length_map = {
        "short": "Summarize clearly in 3–4 sentences.",
        "medium": "Summarize the content in a detailed paragraph.",
        "long": "Summarize thoroughly, capturing all important ideas.",
    }

    instruction = length_map.get(length, length_map["medium"])

    # Step 1: split into chunks
    chunks = split_into_chunks(text, max_chars=3500)

    # Step 2: summarize each chunk
    partial_summaries = []
    for i, chunk in enumerate(chunks):
        part_summary = summarize_chunk(chunk, instruction)
        partial_summaries.append(part_summary)

    # Step 3: combine partial summaries
    combined_text = "\n\n".join(partial_summaries)

    # Step 4: final summary
    final_summary = summarize_chunk(combined_text, "Provide a combined overall summary.")

    return final_summary
