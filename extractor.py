import os
import csv
import pdfplumber
import PyPDF2
import time
from datetime import timedelta



# Function to extract titles from the PDF document outline
def extract_titles(pdf):
    with open(pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        titles = [item.title for item in reader.outline if isinstance(item, PyPDF2.generic.Destination)]

    print(f"Extracted {len(titles)} titles from the document outline")
    return titles

import re

def extract_articles(pdf, titles):
    # Open the PDF file
    with pdfplumber.open(pdf) as pdf:
        full_text = ""
        # Extract all text from the PDF and concatenate into one large string
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"  # Add newline to separate pages

    articles = []
    for title in titles:
        # Create a regex pattern that matches the title ignoring newlines
        # We escape special regex characters in the title and replace spaces with \s+
        escaped_title = re.escape(title).replace(r"\ ", r"\s+")
        title_pattern = re.compile(escaped_title, re.DOTALL)
        
        # Find the start index of the current title
        title_match = title_pattern.search(full_text)
        if not title_match:
            continue  # Title not found, skip to next title

        title_start = title_match.start()

        # Find the start of the article body (after "OpenURL Link")
        body_start = full_text.find("OpenURL Link", title_start)
        if body_start == -1:
            continue  # "OpenURL Link" not found, skip to next title
        body_start = full_text.find("\n", body_start) + 1  # Move to the next line

        # Find the end of the article body (at "Copyright" or "Copyright (c)")
        copyright_index = full_text.find("Copyright,", body_start)
        copyright_c_index = full_text.find("Copyright (c)", body_start)
        copyright_c_c_index = full_text.find("©", body_start)
        copyright_c_c_c_index = full_text.find("Copyright©", body_start)
        body_end = min(index for index in [copyright_index, copyright_c_index, copyright_c_c_index, copyright_c_c_c_index] if index > 0)
        
        if body_end == -1:
            continue  # Copyright not found, skip to next title

        # Extract the article body
        article_body = full_text[body_start:body_end].strip()

        # Add the article to our list
        if article_body:
            print(f"Extracted article: {title}")
            articles.append((title, article_body))

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


    #find the two single number characters in the file name
    numbers_and_pdfs = []
    for pdf in PDFS:
        split_pdf = list(pdf)
        num1, num2 = None, None
        for i in range(len(split_pdf)):
            if split_pdf[i].isdigit():
                if num1 is None:
                    num1 = split_pdf[i]
                else:
                    num2 = split_pdf[i]
                    break

        # print(f"PDF file: {pdf}, Number 1: {num1}, Number 2: {num2}")

        numbers_and_pdfs.append((num1, num2, pdf))

    #sort the list of tuples by num2, then by num1
    numbers_and_pdfs.sort(key=lambda x: (x[1], x[0]))

    print('Found the following PDF files:')
    for pdf in numbers_and_pdfs:
        print('Part:', pdf[1] + ' | Bundle: ' + pdf[0] + ' | Filename:', pdf[2])

    # For each PDF file, open it and extract articles
    for pdf in numbers_and_pdfs:
        titles = extract_titles(pdf[2])
        extracted_articles = extract_articles(pdf[2], titles)
        articles.extend(extracted_articles)
        print(f"Extracted {len(extracted_articles)} articles from {pdf[2]}")

    # Write all articles to a CSV file
    write_to_csv(articles)

    # Metrics
    end_time = time.monotonic()
    time_taken = timedelta(seconds=end_time - start_time)
    print(f"Total articles extracted: {len(articles)}")
    print(f"Time taken: {time_taken}")

if __name__ == "__main__":
    main()