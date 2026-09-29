import pdfplumber
import glob
import csv
import os

def main():
    pdf_files = glob.glob("2000/*.pdf")

    with open("output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Year", "ID", "Title"])

        for file in pdf_files:
            # Extract year from the filename
            basename = os.path.basename(file)
            year = basename.replace(".pdf", "")

            try:
                with pdfplumber.open(file) as pdf:
                    for page in pdf.pages:
                        tables = page.extract_tables()
                        for table in tables:
                            # Iterate over rows in the table
                            for row in table:
                                # Clean the row values by removing newlines and leading/trailing whitespace
                                cleaned_row = [str(cell).replace("\n", " ").strip() if cell is not None else "" for cell in row]

                                # Skip header-like rows or empty rows
                                if len(cleaned_row) >= 2:
                                    if "KORMÁNYHATÁROZATOK" in cleaned_row[0]:
                                        continue
                                    if cleaned_row[0] == "" and cleaned_row[1] == "":
                                        continue

                                    # Output row: Year, ID, Title
                                    writer.writerow([year, cleaned_row[0], cleaned_row[1]])
            except Exception as e:
                print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    main()
