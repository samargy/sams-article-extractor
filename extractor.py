import os
import csv
import pdfplumber
import time
from datetime import timedelta
from tkinter import Tk, Label, Button, filedialog, messagebox

class ArticleExtractorApp:
    def __init__(self, master):
        self.master = master
        master.title("Sam's Article Extractor")

        self.label = Label(master, text="Select the folder containing PDF files:")
        self.label.pack()

        self.select_source_button = Button(master, text="Select Source Folder", command=self.select_source_folder)
        self.select_source_button.pack()

        self.label = Label(master, text="Select the destination folder:")
        self.label.pack()

        self.select_dest_button = Button(master, text="Select Destination Folder", command=self.select_dest_folder)
        self.select_dest_button.pack()

        self.run_button = Button(master, text="Extract Articles", command=self.run_extraction)
        self.run_button.pack()

        self.source_folder = ""
        self.dest_folder = ""

    def select_source_folder(self):
        self.source_folder = filedialog.askdirectory()
        if self.source_folder:
            messagebox.showinfo("Source Folder Selected", f"Source Folder: {self.source_folder}")

    def select_dest_folder(self):
        self.dest_folder = filedialog.askdirectory()
        if self.dest_folder:
            messagebox.showinfo("Destination Folder Selected", f"Destination Folder: {self.dest_folder}")

    def extract_articles(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"

        lines = full_text.splitlines()
        articles = []
        current_title = None
        current_text = []
        collecting_text = False

        for i, line in enumerate(lines):
            if "OpenURL Link" in line:
                if i >= 4:
                    current_title = lines[i - 4].strip()
                current_text = []
                collecting_text = True

            elif "Copyright (c)" in line:
                collecting_text = False
                if current_title and current_text:
                    articles.append((current_title, ' '.join(current_text).strip()))
                current_title = None
                current_text = []

            elif collecting_text:
                current_text.append(line.strip())

        return articles

    def run_extraction(self):
        if not self.source_folder or not self.dest_folder:
            messagebox.showwarning("Folders Not Selected", "Please select both source and destination folders.")
            return

        start_time = time.monotonic()
        articles = []

        pdf_files = [f for f in os.listdir(self.source_folder) if f.endswith(".pdf")]
        if not pdf_files:
            messagebox.showwarning("No PDFs Found", "No PDF files found in the selected source folder.")
            return

        for pdf in pdf_files:
            pdf_path = os.path.join(self.source_folder, pdf)
            extracted_articles = self.extract_articles(pdf_path)
            articles.extend(extracted_articles)
            print(f"Extracted {len(extracted_articles)} articles from {pdf}")

        output_file = os.path.join(self.dest_folder, "articles.csv")
        with open(output_file, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Text'])
            for title, text in articles:
                writer.writerow([title, text])

        end_time = time.monotonic()
        time_taken = timedelta(seconds=end_time - start_time)
        messagebox.showinfo("Extraction Complete", f"Total articles extracted: {len(articles)}\nTime taken: {time_taken}\nSaved to: {output_file}")

def main():
    root = Tk()
    app = ArticleExtractorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
