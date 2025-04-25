import os
import re
import docx
import fitz

from cred import open_ai_key


def extract_from_txt(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()
    

def extract_from_docx(filepath):
    doc = docx.Document(filepath)
    
    return '\n'.join([para.text for para in doc.paragraphs])


def extract_from_pdf(filepath):
    doc = fitz.open(filepath)

    return '\n'.join([page.get_text() for page in doc])


def extract_text(filepath):
    if filepath.endswith('.txt'):
        return extract_from_txt(filepath)
    elif filepath.endswith('.docx'):
        return extract_from_docx(filepath)
    elif filepath.endswith('.pdf'):
        return extract_from_pdf(filepath)
    else:
        raise ValueError("the file format is not supported, please ensure only txt docx or pdf")
    

def generate_summary_and_title(text):
    from openai import OpenAI
    client = OpenAI(api_key=open_ai_key)

    response = client.chat.completions.create(
        model='gpt-4',
        messages = [
            {'role': 'system', 'content': "you summarise documents and suggest title based on the content"},
            {'role': 'user', 'content': f"please suggest a suitable title for this document and try to make it under 10 words:\n {text}"}
        ]
    )

    return response.choices[0].message.content


# enter file path with file extension here
filepath = "C:\External Download\Work Related\AWS Certifications\Mastering College Essays Guidance, Prompts, and Successful Samples.txt"
rename = input("do you want to rename the file or all files inside the path? (y/n): ")
text = extract_text(filepath)
title = generate_summary_and_title(text)
print(title)


if rename == 'y':
    try:
        safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
        base, ext = os.path.splitext(filepath)
        new_filepath = os.path.join(os.path.dirname(filepath), safe_title + ext)

        os.rename(filepath, new_filepath)

        print("\noriginal file name:", os.path.basename(filepath))
        print("renamed file name:", os.path.basename(new_filepath))
        print("location:", os.path.dirname(new_filepath))
    except Exception as e:
        print(f"\nthe renaming for {os.path.basename(filepath)} has failed due to: {e}")
