import pandas as pd
import re

def parse_category_string(cat_str):
    """
    Parses a string like "1. Gazdaságfejlesztés és Vállalati Támogatások (Több nagybefektető)"
    or "7. Külpolitika, EU és Határon Túli Ügyek (EU intézet, jogalkotás) / 2. Nemzetbiztonság"
    into Category, Subcategory, and Explanation.
    """
    cat_str = cat_str.strip()

    # 1. Explanation: everything inside the first pair of parentheses
    explanation_match = re.search(r'\((.*?)\)', cat_str)
    explanation = explanation_match.group(1) if explanation_match else ""

    # Remove the parentheses block for further parsing
    main_part = re.sub(r'\(.*?\)', '', cat_str).strip()

    # We might have multiple categories joined by '/', just take the first for simplicity
    main_part = main_part.split('/')[0].strip()

    # 2. Category: The number and the first word (e.g., "1. Gazdaságfejlesztés")
    parts = main_part.split(' ')
    if len(parts) >= 2 and parts[0].replace('.', '').isdigit():
        category = f"{parts[0]} {parts[1]}"
        # 3. Subcategory: The rest of the string
        subcategory = " ".join(parts[2:]).strip()
    else:
        category = parts[0] if parts else ""
        subcategory = " ".join(parts[1:]).strip()

    return category, subcategory, explanation

def main():
    # 1. Read Markdown file and extract mappings
    mappings = {}
    with open('gemini_categories.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or not line.startswith('|') or 'Azonosító' in line or '---' in line:
            continue

        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 3:
            continue

        id_str = parts[1]
        cat_str = parts[2]

        if not cat_str or cat_str.startswith('2019-től') or cat_str == '':
            continue

        # Parse the category string
        cat, subcat, exp = parse_category_string(cat_str)

        # Handle ranges like 2040/2016 – 2041/2016
        if '–' in id_str or '-' in id_str:
            # normalize dash
            id_str = id_str.replace('–', '-')
            start_id, end_id = [x.strip() for x in id_str.split('-')]

            try:
                start_num, start_year = start_id.split('/')
                end_num, end_year = end_id.split('/')

                if start_year == end_year:
                    for i in range(int(start_num), int(end_num) + 1):
                        current_id = f"{i}/{start_year}"
                        mappings[current_id] = (cat, subcat, exp)
                else:
                    mappings[id_str] = (cat, subcat, exp)
            except Exception:
                mappings[id_str] = (cat, subcat, exp)
        else:
            mappings[id_str] = (cat, subcat, exp)

    # 2. Read existing output.csv
    df = pd.read_csv('output.csv')

    # 3. Apply mappings
    categories = []
    subcategories = []
    explanations = []

    for index, row in df.iterrows():
        decree_id = str(row['ID']).strip()
        if decree_id in mappings:
            c, s, e = mappings[decree_id]
            categories.append(c)
            subcategories.append(s)
            explanations.append(e)
        else:
            categories.append("Other")
            subcategories.append("")
            explanations.append("")

    df['Category'] = categories
    df['Subcategory'] = subcategories
    df['Explanation'] = explanations

    # 4. Save to new CSV
    df.to_csv('output.csv', index=False)
    print("Updated output.csv with new category columns.")

if __name__ == '__main__':
    main()
