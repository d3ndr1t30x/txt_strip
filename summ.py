import os
import argparse
from transformers import pipeline

# Initialize the summarization pipeline with TensorFlow
summarizer = pipeline("summarization", framework="tf")

def summarize_text(text, max_length=150):
    summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def read_file(filename):
    """Read the contents of a text file and return it as a list of paragraphs."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            # Split content into paragraphs based on double newlines
            paragraphs = content.split('\n\n')
            return [para.strip() for para in paragraphs if para.strip()]
    except Exception as e:
        print(f"[Error] Failed to read file: {e}")
        return []

def write_output(filename, summaries):
    """Write the summarized text to the specified output file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for summary in summaries:
                file.write(summary + '\n\n')
    except Exception as e:
        print(f"[Error] Failed to write to output file: {e}")

def main(input_file, output_file):
    paragraphs = read_file(input_file)
    if not paragraphs:
        print("[Error] No paragraphs to summarize.")
        return

    summaries = []
    for paragraph in paragraphs:
        try:
            summary = summarize_text(paragraph)
            summaries.append(summary)
            print(f"[Info] Summarized: {summary}")
        except Exception as e:
            print(f"[Error] Summarization failed for paragraph: {e}")

    write_output(output_file, summaries)
    print(f"[Info] Summarization complete. Output written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Summarize a text file containing paragraphs.')
    parser.add_argument('--input', required=True, help='Input text file with paragraphs.')
    parser.add_argument('--output', required=True, help='Output file for the summarized text.')

    args = parser.parse_args()
    main(args.input, args.output)
