import os
import re
import docx
import fitz

from cred import open_ai_key


# 4: summarise and generate the title for the document
def generate_title(text):
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


# 5: raname the file title
def renaming(title, filepath):
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
    else:
        print(f"suggested title is {title} for {filepath}")


# 3: extract from txt file
def extract_from_txt(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()
    

# 3: extract from docx file
def extract_from_docx(filepath):
    doc = docx.Document(filepath)
    
    return '\n'.join([para.text for para in doc.paragraphs])


# 3: extract from pdf file
def extract_from_pdf(filepath):
    doc = fitz.open(filepath)

    return '\n'.join([page.get_text() for page in doc])


# 2: check whether the file is txt docs or pdf
def process_file(filepath):
    if filepath.endswith('.txt'):
        extracted_texts = extract_from_txt(filepath)
        title = generate_title(extracted_texts)
        renaming(title, filepath)
    elif filepath.endswith('.docx'):
        extracted_texts = extract_from_docx(filepath)
        title = generate_title(extracted_texts)
        renaming(title, filepath)
    elif filepath.endswith('.pdf'):
        extracted_texts = extract_from_pdf(filepath)
        title = generate_title(extracted_texts)
        renaming(title, filepath)
    else:
        print(f"file types not in supported format")
    

# 2: loop through all files in the directory
def loop_folder(filepath):
    try:
        if os.path.isdir(filepath):
            for root, dirs, files in os.walk(filepath):
                for file in files:
                    file_path = os.path.join(root, file)  # getting the full path
                    
                    if file.endswith('.txt'):
                        extracted_texts = extract_from_txt(file_path)
                        title = generate_title(extracted_texts)
                        renaming(title, file_path)
                    elif file.endswith('.docx'):
                        extracted_texts = extract_from_docx(file_path)
                        title = generate_title(extracted_texts)
                        renaming(title, file_path)
                    elif file.endswith('.pdf'):
                        extracted_texts = extract_from_pdf(file_path)
                        title = generate_title(extracted_texts)
                        renaming(title, file_path)
        else:
            print(f"The provided path {filepath} is not a valid folder.")
    except Exception as e:
        print(f"Failed due to error: {e}")


# 1: checking its a file or folder
def file_or_dir(filepath):
    if os.path.isfile(filepath):
        process_file(filepath)
    elif os.path.isdir(filepath):
        loop_folder(filepath)
    else:
        print(f"the path is not file or folder")


# enter file path with file extension here
if __name__ == "__main__":
    filepath = input("enter your file/folder path: ")
    rename = input("do you want to rename the file or all files inside the path? (y/n): ")
    file_or_dir(filepath)
