# GenAI Powerwed Resume Analyzer

## Overview
This tool helps streamline the resume screening process using Generative AI to extract contextual data from a database of resumes and export all the relevant data in a cleanly processed excel sheet. It uses advanced techniques to parse, extract, and evaluate key information from resumes, enabling efficient and scalable pre-analysis for shortlisting candidates. The script uses `gdown` to download files, `pdfplumber` to extract text from PDFs, and OpenAI's GPT-4 model to analyze and summarize the extracted content. The processed data is then saved to an Excel file for further use.

## Features 
- **Automated Resume Parsing**: Extracts mandatory fields such as name, contact details, education, skills, and more.
- **Generative AI Scoring**:
  - *Gen AI Experience Score*: Evaluates experience in generative AI.
  - *AI/ML Experience Score*: Assesses AI/ML proficiency based on resume data.
  - **Batch Processing**: Can handle multiple resumes at a time. 
  - **Output in Structured Format**: Generates a neatly formatted Excel file with extracted data and scores.
- **Context-Aware Extraction**: Leverages GPT models for accurate and relevant data extraction, adapting to various resume formats.

## Installation
- Download all files from the drive
- Install dependencies:
	```bash
    pip install -r requirements.txt
    ```
- Replace the API key in the resumeanalyzer.py script: 
    ```python
    client = OpenAI(api_key="YOURKEY")
    ```
    You can find your API key in the [OpenAI Dashboard](https://platform.openai.com/).

## Usage
- Run the script:
    ```bash
    python resumeanalyzer.py
    ```
- Enter the Google Drive Link containing resumes when prompted:
    ```bash
    Enter the Google Drive folder link:
    ```
- The processed data will be saved as an Excel file (`extracted_resume_data.xlsx`) in the project directory.

## Script Details

### Functions
#### `downloadfolder(drive, output="temp/")`

Downloads all files from a specified Google Drive folder to a temporary directory.

#### `extract(folder_path)`

Extracts text from all PDF files in the given directory.

#### `delete_temp_files(directory)`

Deletes all files and directories created during processing to keep the environment clean.

#### `batch_extract_information(resume_texts)`

Uses OpenAI GPT-4 to analyze and extract key details from resume texts.

#### `parse_key_value_format(raw_response)`

Parses GPT-4 output into structured key-value format for easy storage and processing.

#### `save_to_excel(data, output_path)`

Saves processed resume data to an Excel file.

## Customization

### Batch Size

You can modify the `batch_size` variable in the script to change the number of resumes processed in each batch. Default is `5`. Larger batch sizes might cause issues due to token limits of GPT4. 

### Output File

By default, the processed data is saved as `extracted_resume_data.xlsx`. You can change the `output_excel` variable to specify a different file name or path.

## Dependencies

-   `gdown`: For downloading files from Google Drive.
-   `pdfplumber`: For extracting text from PDF files.
-   `openai`: For GPT-4 integration.
-   `pandas`: For managing and exporting data in tabular form.

## Error Handling

-   **File Download Issues**: Ensure the Google Drive folder link is correct and public access is enabled.
-   **API Key Errors**: Make sure your OpenAI API key is valid and has sufficient quota.

## Future Improvements
- **Improve batch processing**:  Currently due to token limits of GPT4, batch processing over 5 resumes, might case issues. Various methods can be implemented to help improve this, such as asychnronous calls, multiple parallel API calls etc.
- **Functionality**: The functionality can be generalized for different job description and adding job match scores, which will help streamline the hiring process further for different roles. 
## Author

Vignesh Senthilnathan  
vigneshsof02@gmail.com 
[GitHub](https://github.com/senduz)
