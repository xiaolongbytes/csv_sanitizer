import csv
from bs4 import BeautifulSoup
import os

INPUT_DIRECTORY = "input_csvs"
OUTPUT_DIRECTORY = "cleaned_csvs"

TEMP_FILE = 'temp.csv'

BLANK_CELL_SYMBOL = ' '


def create_temp_without_line_breaks(directory: str, file_name: str) -> None:
    """
    Parses CSV file and creates a temp file without erroneous line breaks
    """
    # Read the input CSV and one-lines all html so that html can be stripped
    # This addresses new lines in the html
    with open(os.path.join(directory, file_name), mode='r', encoding='utf-8') as file:
        csv_rows = []
        for line in file:
            cleaned_line = line.strip()
            if len(cleaned_line) < 1:
                continue
            if cleaned_line[0] == "\\":
                continue

            first_char: str = cleaned_line[1]
            if len(csv_rows) > 0 and line[0] == "\"" and first_char.isnumeric():
                csv_rows.append(cleaned_line)

            elif len(csv_rows) > 0 and first_char.isnumeric() is False:
                csv_rows[-1] = csv_rows[-1] + cleaned_line

            if len(csv_rows) == 0:
                csv_rows.append(cleaned_line)

    # Write to temp CSV
    with open(TEMP_FILE, mode='w', newline='', encoding='utf-8') as file:
        for row in csv_rows:
            file.write(row + "\n")


def remove_html_from_temp(directory: str, file_name: str) -> None:
    """
    Parses temp CSV and creates an cleaned CSV without hmtl tags
    """
    # Read the temp CSV
    with open(TEMP_FILE, mode='r', encoding='utf-8') as csv_input:
        csv_reader = csv.reader(csv_input)
        # Store all rows for processing
        rows = list(csv_reader)
        headers = rows[0]
        data = rows[1:]

        # Process each row and strip commas and merge together all html cells
        cleaned_data = []
        for row in data:
            cleaned_row = []
            is_html_cell = False
            html_cell = []
            for cell in row:
                if len(cell) == 0 or cell == "\\N":
                    cleaned_row.append(BLANK_CELL_SYMBOL)
                    continue

                if cell[0] == "<":
                    is_html_cell = True

                if is_html_cell is False:
                    cleaned_row.append(cell)
                else:
                    html_cell.append(cell)

                # Once it find the last html tag, it joins all the html cells together and strips the html
                if cell[-1] == ">" or (len(cell) > 1 and cell[-2] == ">"):
                    is_html_cell = False
                    soup = BeautifulSoup(",".join(html_cell), "html.parser")
                    cleaned_html = soup.get_text()
                    cleaned_row.append(cleaned_html)

            cleaned_data.append(cleaned_row)

        # Write to output CSV
        output_file = "cleaned_" + file_name
        with open(os.path.join(directory, output_file), mode='w', newline='', encoding='utf-8') as csv_output:
            csv_writer = csv.writer(csv_output)
            csv_writer.writerow(headers)
            csv_writer.writerows(cleaned_data)


def clean_csv():
    """
    Creates a cleaned/sanitized CSV in OUTPUT_DIRECTORY for every CSV file in INPUT_DIRECTORY
    """

    for file_name in os.listdir(INPUT_DIRECTORY):
        create_temp_without_line_breaks(INPUT_DIRECTORY, file_name)
        remove_html_from_temp(OUTPUT_DIRECTORY, file_name)


if __name__ == '__main__':
    clean_csv()
