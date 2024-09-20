import csv
import json
import openai
import os

# Set your OpenAI API key here
openai.api_key = ""

def classify_bias(title, text):
    system_prompt = """You are an Australian news article bias classifier. You are to rate both the article headline and text on a scale of:

1 - Very pro-Labor
2 - Somewhat pro-Labor
3 - Middle of the road
4 - Somewhat pro-Coalition
5 - Very pro-Coalition

Here are some things to be looking out for, please keep the following in mind when coding
each paper and headline:

Explicit Signals: These would be the direct and unambiguous use of political
allusions or vocabulary that is consistent with Labor or Liberal discourse. For
example, a headline that openly slanders Tony Abbott's performance in a debate, and
the content positively portrays Malcolm Turnbull, would be some explicit signals.
Another example is the use of the term "tax cuts" and "better living" in the same
sentence, which could be a sign of Labor slant.

Implicit Signals: These might be more subdued instances of prejudice, such the way
a narrative is told, a certain person or event is framed, or the paper's tone. Choosing
selected parts of a tale to stress or presenting particular facts in a good or bad light
based on which political party is involved are two examples of implicit bias. Be
careful of how a paper shapes the occurrence and nature of a potential scandal.

The format you should output your response should be in JSON format.

{
'headline': bias_value,
'text': bias_value,
}"""

    user_prompt = f"Title: {title}\nText: {text}"

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        max_completion_tokens=50  # Added this line
    )

    result = json.loads(response.choices[0].message.content)
    return result['headline'], result['text']

def process_csv(input_file, writer):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            title = row['Title']
            text = row['Text']
            
            title_bias, text_bias = classify_bias(title, text)
            
            row['title_bias'] = title_bias
            row['text_bias'] = text_bias
            
            writer.writerow(row)
            print(f"Processed: {title}")

def process_directory(input_dir, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['Title', 'Text', 'title_bias', 'text_bias']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for filename in os.listdir(input_dir):
            if filename.endswith('.csv'):
                input_path = os.path.join(input_dir, filename)
                process_csv(input_path, writer)
                print(f"Processed file: {filename}")

if __name__ == "__main__":
    input_directory = input("Enter the name of the input directory: ")
    output_file = f"output_{input_directory}_with_bias.csv"
    
    if not os.path.exists(input_directory):
        print(f"Error: The directory '{input_directory}' does not exist.")
    else:
        process_directory(input_directory, output_file)
        print(f"Processing complete. Results saved in {output_file}")