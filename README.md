# csv_sanitizer

## To Install Dependencies:
1. Create & activate your virtual environment
2. Add your virtual environment to the .gitignore file (mine is called `insights`)
3. `pip install -r requirements.txt`

## Problem Statement:
- Received CSV files that contains all the information
    - These CSV files were malformed with the following issues, which required data sanitization:
        - Embedded line breaks/ newlines within fields
        - Escaped HTML content
        - Comma ambiguity
        - Unescaped quotes

## Solution
- `csv_sanitizer.py` is a python script that:
    - Reads all CSV files in a specified input directory
    - Strips embedded line breaks and creates a `temp.csv`
    - Fixes comma ambiguity introduced by HTML content
    - Strips HTML tags
    - Creates a new sanitized CSV file in the specified output directory
