import os
import csv
import pdfplumber
import time
from datetime import timedelta

# Function to extract articles from the PDF
def extract_articles(pdf):
    # Open the PDF file
    with pdfplumber.open(pdf) as pdf:
        full_text = ""
        
        # Extract all text from the PDF and concatenate into one large string
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"  # Add newline to separate pages

    # Split the text into lines
    lines = full_text.splitlines()

    articles = []
    current_title = None
    current_text = []
    collecting_text = False

    for i, line in enumerate(lines):
        if "OpenURL Link" in line:
            if i >= 4:  # Ensure there are at least 4 lines before "OpenURL Link"
                current_title = lines[i - 4].strip()  # Get the title

            # Start collecting text
            current_text = []
            collecting_text = True

        elif "Copyright (c)" in line:
            # Stop collecting text when "Copyright (c)" is found
            collecting_text = False
            if current_title and current_text:
                articles.append((current_title, ' '.join(current_text).strip()))
            current_title = None
            current_text = []

        elif collecting_text:
            current_text.append(line.strip())

    return articles

# Function to write articles to a CSV file
def write_to_csv(articles):
    with open("articles.csv", "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Text'])  # Write header
        for title, text in articles:
            writer.writerow([title, text])

def main():
    start_time = time.monotonic()
    PDFS = []
    articles = []

    # Get the current directory
    current_dir = os.getcwd()

    # Iterate over all files in the directory
    for file in os.listdir(current_dir):
        # Check if the file is a PDF
        if file.endswith(".pdf"):
            # Add the PDF file to the PDFS array
            PDFS.append(file)

    # Print the PDFs
    print(f"PDF files found: {PDFS}")

    # For each PDF file, open it and extract articles
    for pdf in PDFS:
        extracted_articles = extract_articles(pdf)
        articles.extend(extracted_articles)
        print(f"Extracted {len(extracted_articles)} articles from {pdf}")

    # Write all articles to a CSV file
    write_to_csv(articles)

    # Metrics
    end_time = time.monotonic()
    time_taken = timedelta(seconds=end_time - start_time)
    print(f"Total articles extracted: {len(articles)}")
    print(f"Time taken: {time_taken}")

if __name__ == "__main__":
    main()
