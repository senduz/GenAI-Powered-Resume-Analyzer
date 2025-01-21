import os
import gdown
import pdfplumber
from openai import OpenAI
import pandas as pd
import re

client = OpenAI(
  api_key="YOURKEY"
)

def downloadfolder(drive, output="temp/"):
    os.makedirs(output, exist_ok=True)
    gdown.download_folder(drive, quiet=False, output=output)
    print("Files downloaded")
    return output

def extract(folder_path):
    pdf_texts = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(folder_path, file_name)
            with pdfplumber.open(file_path) as pdf:
                text = ''.join(page.extract_text() for page in pdf.pages)
                pdf_texts[file_name] = text
    return pdf_texts

def delete_temp_files(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    os.rmdir(directory)
    print(f"Deleted temporary directory: {directory}")

def batch_extract_information(resume_texts):
    batch_prompt = "\n".join([
        f"Resume {i+1}:\n{resume_text}\nYou are an AI assistant that helps analyze resumes to streamline the hiring process\nExtract the following details in key-value format:\n"
        "Name: <name>\n"
        "Phone Number: <phone number>\n"
        "Email: <email>\n"
        "Address: <address>\n"
        "University: <university>\n"
        "Year of Study: <year of study>\n"
        "Course: <course>\n"
        "Discipline: <discipline>\n"
        "CGPA/Percentage: <cgpa/percentage>\n"
        "Key Skills: <key skills>\n"
        "Gen AI Experience Score: <score>\n"
        "AI/ML Experience Score: <score>\n"
        "Inferred Career Potential: <inferred career>\n"
        "Highlight: <highlight>\n"
        "Other suitable roles: <roles>\n"
        "Supporting Information: <supporting information>\n"
        "Be consistent in formatting to support automated parsing. Maintain concise and relevant responses, avoiding unnecessary details. If any field is missing, use 'NA'.Extract the following details from the provided resume text in a contextual manner. Only copy the relevant information, shorten unnecesary details. Give a resonable GenAI expeirience and AI/ML score. Score can have values 1-3, where 1 – Exposed, 2 – Handson and 3- worked on advanced areas such as Agentic RAG, Evals etc.Similarly for AI/ML experience score as well. The hiring is for interns to help build AI agents in a dynamic, fast paced environment, where the intern will collaborate with the AI team and gain hands on expeirence with cutting edge technologies, Ideal candidates should have a solid grounding in programming and a basic understanding of AI/ML. Fill in the highlight as the best skill they have that matches with our requirement by going through and analyzing the resume. Also analyze their resume thoroughly and find other role they might be suitable for. Keep the scoring consistent and reproducible. Make sure to strictly to the format. Also analyze the resume and add the infered career potential"
        for i, resume_text in enumerate(resume_texts)
    ])

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": batch_prompt}],
        seed=150,
        max_tokens=2000,
        temperature=0
    )
    raw_response = response.choices[0].message.content
    print("Raw API Response:", raw_response)

    return raw_response

def parse_key_value_format(raw_response):
    resumes = re.split(r"Resume \d+:", raw_response)
    parsed_resumes = []
    
    for resume in resumes:
        if resume.strip():
            parsed_data = {}
            lines = resume.strip().split("\n")
            for line in lines:
                if ": " in line:
                    key, value = line.split(": ", 1)
                    parsed_data[key.strip()] = value.strip()
            parsed_resumes.append(parsed_data)
    return parsed_resumes

def save_to_excel(data, output_path):

    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False)
    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    drive = input("Enter the Google Drive folder link: ").strip()
    temp_dir = "temp/"
    output_excel = "extracted_resume_data.xlsx"
    batch_size = 5

    try:
        downloadfolder(drive, temp_dir)
        pdf_texts = extract(temp_dir)

        file_names = list(pdf_texts.keys())
        resume_texts = list(pdf_texts.values())

        all_resumes_data = []
        for i in range(0, len(resume_texts), batch_size):
            batch_texts = resume_texts[i:i + batch_size]
            raw_response = batch_extract_information(batch_texts)
            parsed_resumes = parse_key_value_format(raw_response)

            for file_name, resume_data in zip(file_names[i:i + batch_size], parsed_resumes):
                resume_data["File Name"] = file_name
                all_resumes_data.append(resume_data)

        save_to_excel(all_resumes_data, output_excel)
    finally:
        delete_temp_files(temp_dir)
