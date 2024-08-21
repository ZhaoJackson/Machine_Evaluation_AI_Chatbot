from docx import Document
import csv
import re

def process_document_to_csv(doc_path, reference_csv_path, experiment_csv_path):
    doc = Document(doc_path)
    csv_data = []
    current_heading = ""
    for paragraph in doc.paragraphs:
        if paragraph.text.isupper() or paragraph.style.name.startswith("Heading"):
            current_heading = paragraph.text
        elif paragraph.text.strip():
            csv_data.append([current_heading, paragraph.text])

    processed_csv_data = []
    original_heading = ""
    p1 = p2 = ""
    experiment_counter = 1

    for row in csv_data:
        heading, content = row
        
        if "EXPERIMENT" in heading or "REFERENCE" in heading:
            if p1 and p2:
                processed_csv_data.append([f"{original_heading} - P1", p1])
                processed_csv_data.append([f"{original_heading} - P2", p2])
                processed_csv_data.append([f"{original_heading} - Whole", f"{p1} {p2}"])
                p1 = p2 = ""
            original_heading = re.sub(r":.*", "", heading)

        if not p1:
            p1 = content
        else:
            p2 = content
    if p1 and p2:
        processed_csv_data.append([f"{original_heading} - P1", p1])
        processed_csv_data.append([f"{original_heading} - P2", p2])
        processed_csv_data.append([f"{original_heading} - Whole", f"{p1} {p2}"])

    reference_text_data = []
    experiment_text_data = []

    for row in processed_csv_data:
        heading, content = row
        heading = re.sub(r"( - P1){2}|( - P2){2}|( - Whole){2}", r"\1\2\3", heading)

        if "REFERENCE TEXT" in heading:
            reference_text_data.append([heading, content])
        else:
            experiment_text_data.append([heading, content])

    with open(reference_csv_path, mode='w', newline='', encoding='utf-8') as ref_file:
        writer = csv.writer(ref_file)
        writer.writerow(["Heading", "Content"])
        writer.writerows(reference_text_data)

    with open(experiment_csv_path, mode='w', newline='', encoding='utf-8') as exp_file:
        writer = csv.writer(exp_file)
        writer.writerow(["Heading", "Content"])
        writer.writerows(experiment_text_data)

doc_path = "src/experiments/data_input.docx"
reference_csv_path = "src/experiments/reference_text.csv"
experiment_csv_path = "src/experiments/experiment_text.csv"

process_document_to_csv(doc_path, reference_csv_path, experiment_csv_path)