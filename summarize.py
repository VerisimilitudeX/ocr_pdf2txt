from transformers import pipeline
import os

def chunk_text(text, max_words=500):
    """
    Break text into smaller chunks of approximately `max_words` words.
    """
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize_chunk(chunk, summarizer):
    """
    Summarize a single text chunk using the Hugging Face summarizer.
    """
    try:
        summary = summarizer(chunk, max_length=100, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error summarizing chunk: {e}")
        return ""

def condense_text(input_file, output_file, target_token_limit=70000):
    """
    Condense text from the input file to fit within the specified token limit.
    """
    with open(input_file, "r") as f:
        text = f.read()

    # Break the text into manageable chunks
    chunks = chunk_text(text, max_words=500)

    # Initialize summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Summarize chunks and collect results
    summarized_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i + 1}/{len(chunks)}...")
        summary = summarize_chunk(chunk, summarizer)
        summarized_chunks.append(summary)

    # Combine summaries and truncate to target token limit
    final_text = " ".join(summarized_chunks)
    final_words = final_text.split()[:target_token_limit]
    truncated_text = " ".join(final_words)

    # Save the condensed text to the output file
    with open(output_file, "w") as f:
        f.write(truncated_text)

    print(f"Text successfully condensed to {len(truncated_text.split())} words and saved to {output_file}.")

# Input and output file paths
input_file_path = "/Users/verisimilitude/Documents/GitHub/ocr_pdf2txt/combined_output.txt"
output_file_path = "/Users/verisimilitude/Documents/GitHub/ocr_pdf2txt/condensed_output.txt"

# Condense the text
condense_text(input_file_path, output_file_path, target_token_limit=70000)