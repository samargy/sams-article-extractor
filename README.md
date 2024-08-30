# PDF Article Extraction Script

This script extracts titles and text from news articles stored in PDF files and saves them into a CSV file. It is designed for users with no prior experience with running scripts.

## Prerequisites

Before running the script, you need to ensure the following:

1. **Python Installed**: You need to have Python installed on your computer. You can download it from the official Python website: [Python.org](https://www.python.org).

2. **Required Python Libraries**: The script uses the following Python libraries:
   - pdfplumber
   - csv
   - os
   - time
   - datetime

   You can install the necessary libraries by running the following command in your command line (once Python is installed):
   ```
   pip install pdfplumber
   ```

## Step-by-Step Guide to Run the Script

### 1. Download the Script
Download the `pdf_article_extraction.py` script to a folder on your computer where you want to perform the extraction.

### 2. Prepare Your PDF Files
Place the PDF files that you want to extract articles from in the same folder as the script.

### 3. Open the Command Line
Open the command line interface on your computer:
- Windows: Search for "cmd" or "Command Prompt" in the Start menu.
- Mac/Linux: Open the "Terminal" application.

### 4. Navigate to the Script Folder
Use the `cd` command to navigate to the folder where you saved the script. For example:
```bash
cd path\to\your\folder
```
Replace `path\to\your\folder` with the actual path to the folder containing the script and PDF files.

### 5. Run the Script
Type the following command and press Enter:
```
python pdf_article_extraction.py
```
The script will start running. It will process all the PDF files in the folder, extract the articles, and save them into a CSV file named `articles.csv`.

The command line will display useful metrics such as:
- The number of PDFs processed.
- The number of articles extracted from each PDF.
- The total number of articles extracted.
- The time taken to complete the process.

### 6. Check the Output
Once the script finishes running, you will find a file named `articles.csv` in the same folder as the script. This file contains the extracted titles and text from the PDF files.

You can open this CSV file using any spreadsheet software like Microsoft Excel, Google Sheets, or any text editor.

## Troubleshooting

- **Python Not Recognized**: If you see an error that Python is not recognized, make sure Python is installed and added to your system's PATH. Refer to the Python installation guide for instructions on adding Python to PATH.
- **Missing Libraries**: If you encounter errors related to missing libraries, make sure you installed the required libraries using the `pip install pdfplumber` command.
- **Script Not Running**: Ensure you have navigated to the correct folder in the command line and that the script and PDF files are in the same folder.

## Conclusion

By following these steps, you should be able to run the script and extract articles from your PDF files into a CSV format. If you encounter any issues, feel free to seek help by providing the error message you received.
