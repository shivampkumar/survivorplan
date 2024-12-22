import json
import os
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.cell.cell import MergedCell  # Import MergedCell to handle merged cells
import re

# Define the root directory containing patient directories
ROOT_DIR = '.'  # Update this path if your patient directories are located elsewhere

# Initialize a new Excel workbook
wb = Workbook()

# Define color fills for main sections in Patient Data Sheet
main_section_colors = {
    "Treatment Summary": "FFD3D3D3",  # Light Gray
    "Already Experienced Symptoms or Side Effects": "FFADD8E6",  # Light Blue
    "Cancer Surveillance and Monitoring": "FF90EE90",  # Light Green
    "Lifestyle and Behavior Recommendations": "FFFFE4B5",  # Moccasin
    "Possible Late and Long-term Effects of Cancer Treatment": "FFFFC0CB",  # Pink
    "Possible Other Issues": "FFF0E68C",  # Khaki
    "References to Helpful Resources": "FFE6E6FA",  # Lavender
}

# Define color fills for context sections in Context Data Sheet
context_section_colors = {
    "cancer surveillance and other recommended tests for cancer monitoring": "FFFFA07A",  # Light Salmon
    "lifestyle and behavior recommendations for cancer survivors": "FF98FB98",  # Pale Green
    "possible late and long-term effects of cancer treatment": "FFB0C4DE",  # Light Steel Blue
    "possible other issues that cancer survivors may experience": "FFFFD700",  # Gold
    "references to helpful resources for cancer survivors": "FFDDA0DD",  # Plum
}

# Helper function to sanitize text
def sanitize_text(text):
    """
    Removes illegal characters from a string that cannot be used in Excel cells.
    Specifically, it removes control characters with ASCII codes below 32,
    except for tab (0x09), line feed (0x0A), and carriage return (0x0D).

    Args:
        text (str): The input string to sanitize.

    Returns:
        str: The sanitized string.
    """
    if not isinstance(text, str):
        return text  # If it's not a string, return as is.
    # Remove all control characters except tab, line feed, and carriage return
    return re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', text)

# Helper function to write section headers with color coding and merged cells
def write_section(ws, title, color, row, bold=True, font_size=14, num_columns=7):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=num_columns)
    ws.cell(row=row, column=1, value=title)
    ws.cell(row=row, column=1).font = Font(bold=bold, size=font_size)
    ws.cell(row=row, column=1).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
    ws.cell(row=row, column=1).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    return row + 1

# Helper function to write subsection headers
def write_subsection(ws, title, row, bold=True, font_size=12, num_columns=7):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=num_columns)
    ws.cell(row=row, column=1, value=title)
    ws.cell(row=row, column=1).font = Font(bold=bold, size=font_size)
    ws.cell(row=row, column=1).fill = PatternFill(start_color="FFADD8E6", end_color="FFADD8E6", fill_type="solid")  # Light Blue for subsections
    ws.cell(row=row, column=1).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    return row + 1

# Function to adjust column widths
def adjust_column_widths(ws):
    for col in ws.columns:
        max_length = 0
        column_letter = None
        # Find the first non-merged cell to get the column letter
        for cell in col:
            if not isinstance(cell, MergedCell):
                column_letter = cell.column_letter
                break
        if not column_letter:
            # If all cells in the column are merged, skip adjusting width
            continue
        for cell in col:
            if cell.value:
                cell_length = len(str(cell.value))
                if cell_length > max_length:
                    max_length = cell_length
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column_letter].width = adjusted_width

# Function to process 'treatment_summary.json' as per provided logic
def process_treatment_summary(treatment_ws, json_path, start_row=1):
    """
    Processes the '{i}_treatment_summary.json' file and writes data to the Treatment Summary sheet.

    Args:
        treatment_ws (Worksheet): The Excel worksheet to write the data.
        json_path (str): Path to the '{i}_treatment_summary.json' file.
        start_row (int): The starting row in the worksheet.

    Returns:
        int: The next available row after writing.
    """
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Define color fills for sections
    section_fill = PatternFill(start_color="FFD3D3D3", end_color="FFD3D3D3", fill_type="solid")  # Light gray
    subsection_fill = PatternFill(start_color="FFADD8E6", end_color="FFADD8E6", fill_type="solid")  # Light blue

    # Flags to ensure feedback headers are written only once
    feedback_headers_written = False

    # Helper function to write section headers
    def write_section(title, row):
        treatment_ws.cell(row=row, column=1, value=title)
        treatment_ws.cell(row=row, column=1).font = Font(bold=True, size=14)
        treatment_ws.cell(row=row, column=1).fill = section_fill
        treatment_ws.cell(row=row, column=1).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        return row + 1

    # Helper function to write subsection headers and feedback headers
    def write_subsection_with_feedback(ws, title, row, num_columns=7):
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=num_columns)
        ws.cell(row=row, column=1, value=title)
        ws.cell(row=row, column=1).font = Font(bold=True, size=12)
        ws.cell(row=row, column=1).fill = subsection_fill
        ws.cell(row=row, column=1).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
        row +=1

        # Write data and feedback column headers
        ws.cell(row=row, column=1, value="Field")
        ws.cell(row=row, column=2, value="Value")
        ws.cell(row=row, column=3, value="Is this accurate (True/False)")
        ws.cell(row=row, column=4, value="Comments")
        for col in range(1,5):
            ws.cell(row=row, column=col).font = Font(bold=True)
            ws.cell(row=row, column=col).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        row +=1
        return row

    current_row = start_row

    # Write "Treatment Summary" as the main section
    current_row = write_section("Treatment Summary", current_row)
    current_row += 1  # Add an empty row for spacing

    # 1. Diagnosis
    current_row = write_subsection_with_feedback(treatment_ws, "Diagnosis", current_row)
    diagnosis_list = data.get("Diagnosis", [])
    if diagnosis_list and isinstance(diagnosis_list, list):
        diagnosis = diagnosis_list[0]  # Access the first diagnosis entry
        treatment_ws.cell(row=current_row, column=1, value="Cancer Type")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(diagnosis.get("Cancer Type", "N/A")))
        current_row +=1

        treatment_ws.cell(row=current_row, column=1, value="Diagnosis Date")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(diagnosis.get("Diagnosis Date", "N/A")))
        current_row +=1

        treatment_ws.cell(row=current_row, column=1, value="Cancer Stage")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(diagnosis.get("Cancer Stage", "N/A")))
        current_row +=1

        treatment_ws.cell(row=current_row, column=1, value="Molecular Markers")
        marker = diagnosis.get("Molecular Markers", "")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(marker) if marker else "N/A")
        current_row +=1

        # Leave feedback columns empty for user input
        current_row +=1  # Add a blank row after subsection
    else:
        print(f"No diagnosis data found in '{json_path}'.")
        current_row +=1  # Add spacing even if data is missing

    # 2. Surgery Conducted
    surgery_conducted_list = data.get("Surgery Conducted (Yes/No)", [])
    if surgery_conducted_list and isinstance(surgery_conducted_list, list):
        surgery_conducted = sanitize_text(surgery_conducted_list[0].get("Surgery Conducted (Yes/No)", "N/A"))
    else:
        surgery_conducted = "N/A"
    current_row = write_subsection_with_feedback(treatment_ws, "Surgery Conducted", current_row)
    treatment_ws.cell(row=current_row, column=1, value="Surgery Conducted (Yes/No)")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(surgery_conducted))
    current_row +=1
    # Leave feedback columns empty
    current_row +=1  # Blank row after subsection

    # 3. Surgery Information
    surgery_info_list = data.get("Surgery Information", [])
    if surgery_info_list and isinstance(surgery_info_list, list):
        surgery_info = surgery_info_list[0]  # Access the first surgery entry
    else:
        surgery_info = {}
    current_row = write_subsection_with_feedback(treatment_ws, "Surgery Information", current_row)
    treatment_ws.cell(row=current_row, column=1, value="Procedure")
    procedure = surgery_info.get("Surgery Procedure", "")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(procedure) if procedure else "N/A")
    current_row +=1

    treatment_ws.cell(row=current_row, column=1, value="Date(s) (year)")
    date = surgery_info.get("Surgery Date(s) (year)", "")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(date) if date else "N/A")
    current_row +=1

    treatment_ws.cell(row=current_row, column=1, value="Location")
    location = surgery_info.get("Surgery Location", "")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(location) if location else "N/A")
    current_row +=1

    treatment_ws.cell(row=current_row, column=1, value="Findings")
    findings = surgery_info.get("Surgery Findings", "")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(findings) if findings else "N/A")
    current_row +=1

    # Leave feedback columns empty
    current_row +=1  # Blank row after subsection

    # 4. Radiation Treatment Conducted
    radiation_conducted_list = data.get("Radiation Treatment Conducted (Yes/No)", [])
    if radiation_conducted_list and isinstance(radiation_conducted_list, list):
        radiation_conducted = sanitize_text(radiation_conducted_list[0].get("Radiation Treatment Conducted (Yes/No)", "N/A"))
    else:
        radiation_conducted = "N/A"
    current_row = write_subsection_with_feedback(treatment_ws, "Radiation Treatment Conducted", current_row)
    treatment_ws.cell(row=current_row, column=1, value="Radiation Treatment Conducted (Yes/No)")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(radiation_conducted))
    current_row +=1
    # Leave feedback columns empty
    current_row +=1  # Blank row after subsection

    # 5. Radiation Treatment Information
    radiation_info_list = data.get("Radiation Treatment Information", [])
    if radiation_info_list and isinstance(radiation_info_list, list):
        radiation_info = radiation_info_list[0]  # Access the first radiation entry
    else:
        radiation_info = {}
    current_row = write_subsection_with_feedback(treatment_ws, "Radiation Treatment Information", current_row)
    treatment_ws.cell(row=current_row, column=1, value="Procedure")
    rad_procedure = radiation_info.get("Radiation Treatment Procedure", "")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(rad_procedure) if rad_procedure else "N/A")
    current_row +=1

    treatment_ws.cell(row=current_row, column=1, value="Date(s) (year)")
    rad_date = radiation_info.get("Radiation Treatment Date(s) (year)", "")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(rad_date) if rad_date else "N/A")
    current_row +=1

    treatment_ws.cell(row=current_row, column=1, value="Location")
    rad_location = radiation_info.get("Radiation Treatment Location", "")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(rad_location) if rad_location else "N/A")
    current_row +=1

    # Leave feedback columns empty
    current_row +=1  # Blank row after subsection

    # 6. Systemic Therapy Conducted
    systemic_conducted_list = data.get("Systemic Therapy Conducted (Chemotherapy, hormonal therapy, other)", [])
    if systemic_conducted_list and isinstance(systemic_conducted_list, list):
        systemic_conducted = sanitize_text(systemic_conducted_list[0].get("Systemic Therapy Conducted (Chemotherapy, hormonal therapy, other)", "N/A"))
    else:
        systemic_conducted = "N/A"
    current_row = write_subsection_with_feedback(treatment_ws, "Systemic Therapy Conducted (Chemotherapy, hormonal therapy, other)", current_row)
    treatment_ws.cell(row=current_row, column=1, value="Systemic Therapy Conducted (Chemotherapy, hormonal therapy, other)")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(systemic_conducted))
    current_row +=1
    # Leave feedback columns empty
    current_row +=1  # Blank row after subsection

    # 7. Agents Used in Completed Treatments
    current_row = write_subsection_with_feedback(treatment_ws, "Agents Used in Completed Treatments", current_row)
    agents = data.get("Agents Used in Completed Treatments", [])
    for agent in agents:
        treatment_ws.cell(row=current_row, column=1, value="Agent Name")
        treatment_ws.cell(row=current_row, column=2, value=agent.get("Agent Name", "N/A"))
        current_row +=1

        treatment_ws.cell(row=current_row, column=1, value="End Date")
        end_date = agent.get("End Date", "")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(end_date) if end_date else "N/A")
        current_row +=1

        # Leave feedback columns empty
    current_row +=1  # Blank row after subsection

    # 8. Persistent Symptoms or Side Effects at Completion of Treatment
    persistent_symptoms_list = data.get("Persistent Symptoms or Side Effects at Completion of Treatment (Yes/No)", [])
    if persistent_symptoms_list and isinstance(persistent_symptoms_list, list):
        persistent_symptoms = sanitize_text(persistent_symptoms_list[0].get("Persistent Symptoms or Side Effects at Completion of Treatment (Yes/No)", "N/A"))
    else:
        persistent_symptoms = "N/A"
    current_row = write_subsection_with_feedback(treatment_ws, "Persistent Symptoms or Side Effects at Completion of Treatment", current_row)
    treatment_ws.cell(row=current_row, column=1, value="Persistent Symptoms or Side Effects at Completion of Treatment (Yes/No)")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(persistent_symptoms))
    current_row +=1
    # Leave feedback columns empty
    current_row +=1  # Blank row after subsection

    # 9. Symptoms or Side Effects
    current_row = write_subsection_with_feedback(treatment_ws, "Symptoms or Side Effects", current_row)
    symptoms = data.get("Symptoms or Side Effects", [])
    for symptom in symptoms:
        treatment_ws.cell(row=current_row, column=1, value="Side Effect")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(symptom.get("Side Effect", "N/A")))
        current_row +=1
        # Leave feedback columns empty
    current_row +=1  # Blank row after subsection

    # 10. Need for Ongoing (Adjuvant) Treatment for Cancer
    need_ongoing_list = data.get("Need for Ongoing (Adjuvant) Treatment for Cancer (Yes/No)", [])
    if need_ongoing_list and isinstance(need_ongoing_list, list):
        need_ongoing = sanitize_text(need_ongoing_list[0].get("Need for Ongoing (Adjuvant) Treatment for Cancer (Yes/No)", "N/A"))
    else:
        need_ongoing = "N/A"
    current_row = write_subsection_with_feedback(treatment_ws, "Need for Ongoing (Adjuvant) Treatment for Cancer", current_row)
    treatment_ws.cell(row=current_row, column=1, value="Need for Ongoing (Adjuvant) Treatment for Cancer (Yes/No)")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(need_ongoing))
    current_row +=1
    # Leave feedback columns empty
    current_row +=1  # Blank row after subsection

    # 11. Ongoing Treatment Information
    ongoing_info_list = data.get("Ongoing Treatment Information", [])
    if ongoing_info_list and isinstance(ongoing_info_list, list):
        ongoing_info = ongoing_info_list[0]  # Access the first ongoing treatment entry
    else:
        ongoing_info = {}
    current_row = write_subsection_with_feedback(treatment_ws, "Ongoing Treatment Information", current_row)
    treatment_ws.cell(row=current_row, column=1, value="Ongoing Treatment")
    ongoing = ongoing_info.get("Ongoing Treatment", "")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(ongoing) if ongoing else "N/A")
    current_row +=1

    treatment_ws.cell(row=current_row, column=1, value="Planned Duration")
    planned_duration = ongoing_info.get("Planned Duration", "")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(planned_duration) if planned_duration else "N/A")
    current_row +=1

    treatment_ws.cell(row=current_row, column=1, value="Possible Side Effects")
    possible_side = ongoing_info.get("Possible Side Effects", "")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(possible_side) if possible_side else "N/A")
    current_row +=1

    # Leave feedback columns empty
    current_row +=1  # Blank row after subsection

    # 12. Additional Comments
    current_row = write_subsection_with_feedback(treatment_ws, "Additional Comments", current_row)
    additional_comments = data.get("Additional Comments", "")
    treatment_ws.cell(row=current_row, column=1, value="Additional Comments")
    treatment_ws.cell(row=current_row, column=2, value=sanitize_text(additional_comments))
    treatment_ws.cell(row=current_row, column=2).alignment = Alignment(wrap_text=True)
    current_row +=1
    # Leave feedback columns empty

    # Adjust column widths
    for column_cells in treatment_ws.columns:
        length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
        adjusted_width = (length + 2)
        treatment_ws.column_dimensions[column_cells[0].column_letter].width = adjusted_width

    return current_row

# ----------------------------
# 4. Process Multiple Patients
# ----------------------------

# Define the range of patient indices
PATIENT_INDICES = range(0, 40)  # 0 to 39

for i in PATIENT_INDICES:
    print(f"Processing Patient {i}...")
    patient_dir = os.path.join(ROOT_DIR, str(i))
    if not os.path.isdir(patient_dir):
        print(f"Directory '{patient_dir}' does not exist. Skipping Patient {i}.")
        continue

    # Define main_to_context_files mapping for patient i
    main_to_context_files = {
        f'{i}_treatment_summary.json': None,
        f'{i}_Already experienced symptoms or side effects.json': None,
        f'{i}_Cancer surveillance and other recommended tests for cancer monitoring.json':
            f'{i}_retrieved_context_Cancer surveillance and other recommended tests for cancer monitoring.json',
        f'{i}_Lifestyle and behavior recommendations for cancer survivors.json':
            f'{i}_retrieved_context_Lifestyle and behavior recommendations for cancer survivors.json',
        f'{i}_Possible late and long-term effects of cancer treatment.json':
            f'{i}_retrieved_context_Possible late and long-term effects of cancer treatment.json',
        f'{i}_Possible other issues that cancer survivors may experience.json':
            f'{i}_retrieved_context_Possible other issues that cancer survivors may experience.json',
        f'{i}_References to helpful resources for cancer survivors.json':
            f'{i}_retrieved_context_References to helpful resources for cancer survivors.json',
    }

    # Create sheets for patient i
    context_sheet_name = f"{i}_Context Data"
    patient_sheet_name = f"{i}_Patient Data"
    treatment_sheet_name = f"{i}_Treatment Summary"

    # Create Context Data sheet
    if context_sheet_name in wb.sheetnames:
        context_ws = wb[context_sheet_name]
    else:
        context_ws = wb.create_sheet(title=context_sheet_name)

    # Create Patient Data sheet
    if patient_sheet_name in wb.sheetnames:
        patient_ws = wb[patient_sheet_name]
    else:
        patient_ws = wb.create_sheet(title=patient_sheet_name)

    # Create Treatment Summary sheet
    if treatment_sheet_name in wb.sheetnames:
        treatment_ws = wb[treatment_sheet_name]
    else:
        treatment_ws = wb.create_sheet(title=treatment_sheet_name)

    # Dictionary to map (information_category, context_id) to cell address in Context Data Sheet
    context_links = {}

    # ----------------------------
    # 1. Process Retrieved Context Data
    # ----------------------------

    for main_file, context_file in main_to_context_files.items():
        main_path = os.path.join(patient_dir, main_file)
        context_path = os.path.join(patient_dir, context_file) if context_file else None

        if context_file and os.path.exists(context_path):
            with open(context_path, 'r') as cf:
                context_json = json.load(cf)

            # Extract information_category from context file name
            information_category = context_file.replace(f'{i}_retrieved_context_', '').replace('.json', '').strip().lower()

            # Get color for context section
            context_color = context_section_colors.get(information_category, "FFFFE4E1")  # Default to Misty Rose

            # Write section header for context category
            context_current_row = write_section(context_ws, f"{information_category.title()}", context_color, context_ws.max_row + 1)

            # Write column headers
            headers = ["ContextID", "Page Number", "Document Title", "Keywords", "Information Category", "Source", "Text"]
            for col_num, header in enumerate(headers, start=1):
                context_ws.cell(row=context_current_row, column=col_num, value=header)
                context_ws.cell(row=context_current_row, column=col_num).font = Font(bold=True)
                context_ws.cell(row=context_current_row, column=col_num).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            context_current_row +=1

            retrieved_context = context_json.get("retrieved_context", {})
            for ctx_id, ctx_content in retrieved_context.items():
                metadata = ctx_content.get("metadata", {})
                text = sanitize_text(ctx_content.get("text", "N/A"))

                # Write the entry row
                context_ws.cell(row=context_current_row, column=1, value=sanitize_text(ctx_id))  # ContextID
                context_ws.cell(row=context_current_row, column=2, value=sanitize_text(metadata.get("page_number", "N/A")))
                context_ws.cell(row=context_current_row, column=3, value=sanitize_text(metadata.get("doc_title", "N/A")))
                keywords = metadata.get("keywords", [])
                keywords_sanitized = ', '.join([sanitize_text(k) for k in keywords]) if keywords else "N/A"
                context_ws.cell(row=context_current_row, column=4, value=keywords_sanitized)
                context_ws.cell(row=context_current_row, column=5, value=sanitize_text(metadata.get("information_category", "N/A")))
                context_ws.cell(row=context_current_row, column=6, value=sanitize_text(metadata.get("source", "N/A")))
                context_ws.cell(row=context_current_row, column=7, value=text)
                context_ws.cell(row=context_current_row, column=7).alignment = Alignment(wrap_text=True)

                # Apply alternating row colors for entries
                if context_current_row % 2 == 0:
                    fill_color = "FFF2F2F2"  # Light Gray for even rows
                else:
                    fill_color = "FFFFFFFF"  # White for odd rows
                for col in range(1, 8):
                    context_ws.cell(row=context_current_row, column=col).fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")

                # Record the cell address for this context ID (pointing to the 'ContextID' column)
                cell_address = f"{get_column_letter(1)}{context_current_row}"  # Column 1 is 'ContextID'
                context_links[(information_category, str(ctx_id))] = cell_address

                context_current_row +=1

            # Add spacing after each section
            context_current_row +=1

        elif context_file:
            print(f"Context JSON file '{context_path}' for main file '{main_file}' does not exist. Skipping context data.")
        else:
            # Main file has no corresponding context JSON file
            continue

    # ----------------------------
    # 2. Process Treatment Summary
    # ----------------------------

    def process_treatment_summary(treatment_ws, json_path, start_row=1):
        """
        Processes the '{i}_treatment_summary.json' file and writes data to the Treatment Summary sheet.

        Args:
            treatment_ws (Worksheet): The Excel worksheet to write the data.
            json_path (str): Path to the '{i}_treatment_summary.json' file.
            start_row (int): The starting row in the worksheet.

        Returns:
            int: The next available row after writing.
        """
        with open(json_path, 'r') as file:
            data = json.load(file)

        # Define color fills for sections
        section_fill = PatternFill(start_color="FFD3D3D3", end_color="FFD3D3D3", fill_type="solid")  # Light gray
        subsection_fill = PatternFill(start_color="FFADD8E6", end_color="FFADD8E6", fill_type="solid")  # Light blue

        # Flags to ensure feedback headers are written only once
        feedback_headers_written = False

        # Helper function to write section headers
        def write_section(title, row):
            treatment_ws.cell(row=row, column=1, value=title)
            treatment_ws.cell(row=row, column=1).font = Font(bold=True, size=14)
            treatment_ws.cell(row=row, column=1).fill = section_fill
            treatment_ws.cell(row=row, column=1).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            return row + 1

        # Helper function to write subsection headers and feedback headers
        def write_subsection_with_feedback(ws, title, row, num_columns=7):
            ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=num_columns)
            ws.cell(row=row, column=1, value=title)
            ws.cell(row=row, column=1).font = Font(bold=True, size=12)
            ws.cell(row=row, column=1).fill = subsection_fill
            ws.cell(row=row, column=1).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
            row +=1

            # Write data and feedback column headers
            ws.cell(row=row, column=1, value="Field")
            ws.cell(row=row, column=2, value="Value")
            ws.cell(row=row, column=3, value="Is this accurate (True/False)")
            ws.cell(row=row, column=4, value="Comments")
            for col in range(1,5):
                ws.cell(row=row, column=col).font = Font(bold=True)
                ws.cell(row=row, column=col).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            row +=1
            return row

        current_row = start_row

        # Write "Treatment Summary" as the main section
        current_row = write_section("Treatment Summary", current_row)
        current_row += 1  # Add an empty row for spacing

        # 1. Diagnosis
        current_row = write_subsection_with_feedback(treatment_ws, "Diagnosis", current_row)
        diagnosis_list = data.get("Diagnosis", [])
        if diagnosis_list and isinstance(diagnosis_list, list):
            diagnosis = diagnosis_list[0]  # Access the first diagnosis entry
            treatment_ws.cell(row=current_row, column=1, value="Cancer Type")
            treatment_ws.cell(row=current_row, column=2, value=sanitize_text(diagnosis.get("Cancer Type", "N/A")))
            current_row +=1

            treatment_ws.cell(row=current_row, column=1, value="Diagnosis Date")
            treatment_ws.cell(row=current_row, column=2, value=sanitize_text(diagnosis.get("Diagnosis Date", "N/A")))
            current_row +=1

            treatment_ws.cell(row=current_row, column=1, value="Cancer Stage")
            treatment_ws.cell(row=current_row, column=2, value=sanitize_text(diagnosis.get("Cancer Stage", "N/A")))
            current_row +=1

            treatment_ws.cell(row=current_row, column=1, value="Molecular Markers")
            marker = diagnosis.get("Molecular Markers", "")
            treatment_ws.cell(row=current_row, column=2, value=sanitize_text(marker) if marker else "N/A")
            current_row +=1

            # Leave feedback columns empty for user input
            current_row +=1  # Add a blank row after subsection
        else:
            print(f"No diagnosis data found in '{json_path}'.")
            current_row +=1  # Add spacing even if data is missing

        # 2. Surgery Conducted
        surgery_conducted_list = data.get("Surgery Conducted (Yes/No)", [])
        if surgery_conducted_list and isinstance(surgery_conducted_list, list):
            surgery_conducted = sanitize_text(surgery_conducted_list[0].get("Surgery Conducted (Yes/No)", "N/A"))
        else:
            surgery_conducted = "N/A"
        current_row = write_subsection_with_feedback(treatment_ws, "Surgery Conducted", current_row)
        treatment_ws.cell(row=current_row, column=1, value="Surgery Conducted (Yes/No)")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(surgery_conducted))
        current_row +=1
        # Leave feedback columns empty
        current_row +=1  # Blank row after subsection

        # 3. Surgery Information
        surgery_info_list = data.get("Surgery Information", [])
        if surgery_info_list and isinstance(surgery_info_list, list):
            surgery_info = surgery_info_list[0]  # Access the first surgery entry
        else:
            surgery_info = {}
        current_row = write_subsection_with_feedback(treatment_ws, "Surgery Information", current_row)
        treatment_ws.cell(row=current_row, column=1, value="Procedure")
        procedure = surgery_info.get("Surgery Procedure", "")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(procedure) if procedure else "N/A")
        current_row +=1

        treatment_ws.cell(row=current_row, column=1, value="Date(s) (year)")
        date = surgery_info.get("Surgery Date(s) (year)", "")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(date) if date else "N/A")
        current_row +=1

        treatment_ws.cell(row=current_row, column=1, value="Location")
        location = surgery_info.get("Surgery Location", "")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(location) if location else "N/A")
        current_row +=1

        treatment_ws.cell(row=current_row, column=1, value="Findings")
        findings = surgery_info.get("Surgery Findings", "")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(findings) if findings else "N/A")
        current_row +=1

        # Leave feedback columns empty
        current_row +=1  # Blank row after subsection

        # 4. Radiation Treatment Conducted
        radiation_conducted_list = data.get("Radiation Treatment Conducted (Yes/No)", [])
        if radiation_conducted_list and isinstance(radiation_conducted_list, list):
            radiation_conducted = sanitize_text(radiation_conducted_list[0].get("Radiation Treatment Conducted (Yes/No)", "N/A"))
        else:
            radiation_conducted = "N/A"
        current_row = write_subsection_with_feedback(treatment_ws, "Radiation Treatment Conducted", current_row)
        treatment_ws.cell(row=current_row, column=1, value="Radiation Treatment Conducted (Yes/No)")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(radiation_conducted))
        current_row +=1
        # Leave feedback columns empty
        current_row +=1  # Blank row after subsection

        # 5. Radiation Treatment Information
        radiation_info_list = data.get("Radiation Treatment Information", [])
        if radiation_info_list and isinstance(radiation_info_list, list):
            radiation_info = radiation_info_list[0]  # Access the first radiation entry
        else:
            radiation_info = {}
        current_row = write_subsection_with_feedback(treatment_ws, "Radiation Treatment Information", current_row)
        treatment_ws.cell(row=current_row, column=1, value="Procedure")
        rad_procedure = radiation_info.get("Radiation Treatment Procedure", "")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(rad_procedure) if rad_procedure else "N/A")
        current_row +=1

        treatment_ws.cell(row=current_row, column=1, value="Date(s) (year)")
        rad_date = radiation_info.get("Radiation Treatment Date(s) (year)", "")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(rad_date) if rad_date else "N/A")
        current_row +=1

        treatment_ws.cell(row=current_row, column=1, value="Location")
        rad_location = radiation_info.get("Radiation Treatment Location", "")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(rad_location) if rad_location else "N/A")
        current_row +=1

        # Leave feedback columns empty
        current_row +=1  # Blank row after subsection

        # 6. Systemic Therapy Conducted
        systemic_conducted_list = data.get("Systemic Therapy Conducted (Chemotherapy, hormonal therapy, other)", [])
        if systemic_conducted_list and isinstance(systemic_conducted_list, list):
            systemic_conducted = sanitize_text(systemic_conducted_list[0].get("Systemic Therapy Conducted (Chemotherapy, hormonal therapy, other)", "N/A"))
        else:
            systemic_conducted = "N/A"
        current_row = write_subsection_with_feedback(treatment_ws, "Systemic Therapy Conducted (Chemotherapy, hormonal therapy, other)", current_row)
        treatment_ws.cell(row=current_row, column=1, value="Systemic Therapy Conducted (Chemotherapy, hormonal therapy, other)")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(systemic_conducted))
        current_row +=1
        # Leave feedback columns empty
        current_row +=1  # Blank row after subsection

        # 7. Agents Used in Completed Treatments
        current_row = write_subsection_with_feedback(treatment_ws, "Agents Used in Completed Treatments", current_row)
        agents = data.get("Agents Used in Completed Treatments", [])
        for agent in agents:
            treatment_ws.cell(row=current_row, column=1, value="Agent Name")
            treatment_ws.cell(row=current_row, column=2, value=agent.get("Agent Name", "N/A"))
            current_row +=1

            treatment_ws.cell(row=current_row, column=1, value="End Date")
            end_date = agent.get("End Date", "")
            treatment_ws.cell(row=current_row, column=2, value=sanitize_text(end_date) if end_date else "N/A")
            current_row +=1

            # Leave feedback columns empty
        current_row +=1  # Blank row after subsection

        # 8. Persistent Symptoms or Side Effects at Completion of Treatment
        persistent_symptoms_list = data.get("Persistent Symptoms or Side Effects at Completion of Treatment (Yes/No)", [])
        if persistent_symptoms_list and isinstance(persistent_symptoms_list, list):
            persistent_symptoms = sanitize_text(persistent_symptoms_list[0].get("Persistent Symptoms or Side Effects at Completion of Treatment (Yes/No)", "N/A"))
        else:
            persistent_symptoms = "N/A"
        current_row = write_subsection_with_feedback(treatment_ws, "Persistent Symptoms or Side Effects at Completion of Treatment", current_row)
        treatment_ws.cell(row=current_row, column=1, value="Persistent Symptoms or Side Effects at Completion of Treatment (Yes/No)")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(persistent_symptoms))
        current_row +=1
        # Leave feedback columns empty
        current_row +=1  # Blank row after subsection

        # 9. Symptoms or Side Effects
        current_row = write_subsection_with_feedback(treatment_ws, "Symptoms or Side Effects", current_row)
        symptoms = data.get("Symptoms or Side Effects", [])
        for symptom in symptoms:
            treatment_ws.cell(row=current_row, column=1, value="Side Effect")
            treatment_ws.cell(row=current_row, column=2, value=sanitize_text(symptom.get("Side Effect", "N/A")))
            current_row +=1
            # Leave feedback columns empty
        current_row +=1  # Blank row after subsection

        # 10. Need for Ongoing (Adjuvant) Treatment for Cancer
        need_ongoing_list = data.get("Need for Ongoing (Adjuvant) Treatment for Cancer (Yes/No)", [])
        if need_ongoing_list and isinstance(need_ongoing_list, list):
            need_ongoing = sanitize_text(need_ongoing_list[0].get("Need for Ongoing (Adjuvant) Treatment for Cancer (Yes/No)", "N/A"))
        else:
            need_ongoing = "N/A"
        current_row = write_subsection_with_feedback(treatment_ws, "Need for Ongoing (Adjuvant) Treatment for Cancer", current_row)
        treatment_ws.cell(row=current_row, column=1, value="Need for Ongoing (Adjuvant) Treatment for Cancer (Yes/No)")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(need_ongoing))
        current_row +=1
        # Leave feedback columns empty
        current_row +=1  # Blank row after subsection

        # 11. Ongoing Treatment Information
        ongoing_info_list = data.get("Ongoing Treatment Information", [])
        if ongoing_info_list and isinstance(ongoing_info_list, list):
            ongoing_info = ongoing_info_list[0]  # Access the first ongoing treatment entry
        else:
            ongoing_info = {}
        current_row = write_subsection_with_feedback(treatment_ws, "Ongoing Treatment Information", current_row)
        treatment_ws.cell(row=current_row, column=1, value="Ongoing Treatment")
        ongoing = ongoing_info.get("Ongoing Treatment", "")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(ongoing) if ongoing else "N/A")
        current_row +=1

        treatment_ws.cell(row=current_row, column=1, value="Planned Duration")
        planned_duration = ongoing_info.get("Planned Duration", "")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(planned_duration) if planned_duration else "N/A")
        current_row +=1

        treatment_ws.cell(row=current_row, column=1, value="Possible Side Effects")
        possible_side = ongoing_info.get("Possible Side Effects", "")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(possible_side) if possible_side else "N/A")
        current_row +=1

        # Leave feedback columns empty
        current_row +=1  # Blank row after subsection

        # 12. Additional Comments
        current_row = write_subsection_with_feedback(treatment_ws, "Additional Comments", current_row)
        treatment_ws.cell(row=current_row, column=1, value="Additional Comments")
        treatment_ws.cell(row=current_row, column=2, value=sanitize_text(additional_comments))
        treatment_ws.cell(row=current_row, column=2).alignment = Alignment(wrap_text=True)
        current_row +=1
        # Leave feedback columns empty

        # Adjust column widths
        for column_cells in treatment_ws.columns:
            length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
            adjusted_width = (length + 2)
            treatment_ws.column_dimensions[column_cells[0].column_letter].width = adjusted_width

        return current_row

    # Process Treatment Summary
    for i in PATIENT_INDICES:
        patient_dir = os.path.join(ROOT_DIR, str(i))
        treatment_summary_file = f'{i}_treatment_summary.json'
        treatment_summary_path = os.path.join(patient_dir, treatment_summary_file)
        if os.path.exists(treatment_summary_path):
            treatment_ws = wb[f"{i}_Treatment Summary"]
            process_treatment_summary(treatment_ws, treatment_summary_path)
        else:
            print(f"Treatment summary file '{treatment_summary_path}' does not exist for Patient {i}.")

    # ----------------------------
    # 3. Process Main Patient Data
    # ----------------------------

    # Helper function to write section headers with color coding
    def write_patient_section(ws, title, color, row, bold=True, font_size=14):
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)  # Update to span all 6 columns
        ws.cell(row=row, column=1, value=title)
        ws.cell(row=row, column=1).font = Font(bold=bold, size=font_size)
        ws.cell(row=row, column=1).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
        ws.cell(row=row, column=1).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
        return row + 1

    # Helper function to write subsection headers and feedback headers
    def write_patient_subsection_with_feedback(ws, title, row, num_columns=6):
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=num_columns)
        ws.cell(row=row, column=1, value=title)
        ws.cell(row=row, column=1).font = Font(bold=True, size=12)
        ws.cell(row=row, column=1).fill = PatternFill(start_color="FFADD8E6", end_color="FFADD8E6", fill_type="solid")  # Light Blue for subsections
        ws.cell(row=row, column=1).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
        row +=1

        # Write data and feedback column headers
        ws.cell(row=row, column=1, value="Question")
        ws.cell(row=row, column=2, value="Answer")
        ws.cell(row=row, column=3, value="Is this recommendation correct? (0-5)")
        ws.cell(row=row, column=4, value="Is it backed by the guidelines? True or False")
        ws.cell(row=row, column=5, value="Is it actionable? (0-5)")
        ws.cell(row=row, column=6, value="Comments")
        for col in range(1,7):
            ws.cell(row=row, column=col).font = Font(bold=True)
            ws.cell(row=row, column=col).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        row +=1
        return row

    # Helper function to write overall feedback in Patient Data sheet
    def write_overall_feedback(ws, row):
        feedback_questions = [
            "Is this customized to the patients' needs (0-5)",
            "Clarity and understandability (0-5)",
            "Comprehensiveness (0-5)",
            "Comments"
        ]

        for question in feedback_questions:
            ws.cell(row=row, column=1, value=question)
            ws.cell(row=row, column=2, value="")  # Leave blank for input
            # Optionally, merge cells or format as needed
            ws.cell(row=row, column=1).font = Font(bold=True)
            ws.cell(row=row, column=1).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
            row +=1
        return row

    for i in PATIENT_INDICES:
        patient_dir = os.path.join(ROOT_DIR, str(i))
        if not os.path.isdir(patient_dir):
            print(f"Directory '{patient_dir}' does not exist. Skipping Patient {i}.")
            continue

        # Define main_to_context_files mapping for patient i
        main_to_context_files = {
            f'{i}_treatment_summary.json': None,
            f'{i}_Already experienced symptoms or side effects.json': None,
            f'{i}_Cancer surveillance and other recommended tests for cancer monitoring.json':
                f'{i}_retrieved_context_Cancer surveillance and other recommended tests for cancer monitoring.json',
            f'{i}_Lifestyle and behavior recommendations for cancer survivors.json':
                f'{i}_retrieved_context_Lifestyle and behavior recommendations for cancer survivors.json',
            f'{i}_Possible late and long-term effects of cancer treatment.json':
                f'{i}_retrieved_context_Possible late and long-term effects of cancer treatment.json',
            f'{i}_Possible other issues that cancer survivors may experience.json':
                f'{i}_retrieved_context_Possible other issues that cancer survivors may experience.json',
            f'{i}_References to helpful resources for cancer survivors.json':
                f'{i}_retrieved_context_References to helpful resources for cancer survivors.json',
        }

        # Create sheets for patient i
        context_sheet_name = f"{i}_Context Data"
        patient_sheet_name = f"{i}_Patient Data"
        treatment_sheet_name = f"{i}_Treatment Summary"

        # Create Context Data sheet
        if context_sheet_name in wb.sheetnames:
            context_ws = wb[context_sheet_name]
        else:
            context_ws = wb.create_sheet(title=context_sheet_name)

        # Create Patient Data sheet
        if patient_sheet_name in wb.sheetnames:
            patient_ws = wb[patient_sheet_name]
        else:
            patient_ws = wb.create_sheet(title=patient_sheet_name)

        # Create Treatment Summary sheet
        if treatment_sheet_name in wb.sheetnames:
            treatment_ws = wb[treatment_sheet_name]
        else:
            treatment_ws = wb.create_sheet(title=treatment_sheet_name)

        # Dictionary to map (information_category, context_id) to cell address in Context Data Sheet
        context_links = {}

        # ----------------------------
        # 1. Process Retrieved Context Data
        # ----------------------------

        for main_file, context_file in main_to_context_files.items():
            main_path = os.path.join(patient_dir, main_file)
            context_path = os.path.join(patient_dir, context_file) if context_file else None

            if context_file and os.path.exists(context_path):
                with open(context_path, 'r') as cf:
                    context_json = json.load(cf)

                # Extract information_category from context file name
                information_category = context_file.replace(f'{i}_retrieved_context_', '').replace('.json', '').strip().lower()

                # Get color for context section
                context_color = context_section_colors.get(information_category, "FFFFE4E1")  # Default to Misty Rose

                # Write section header for context category
                context_current_row = write_section(context_ws, f"{information_category.title()}", context_color, context_ws.max_row + 1)

                # Write column headers
                headers = ["ContextID", "Page Number", "Document Title", "Keywords", "Information Category", "Source", "Text"]
                for col_num, header in enumerate(headers, start=1):
                    context_ws.cell(row=context_current_row, column=col_num, value=header)
                    context_ws.cell(row=context_current_row, column=col_num).font = Font(bold=True)
                    context_ws.cell(row=context_current_row, column=col_num).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                context_current_row +=1

                retrieved_context = context_json.get("retrieved_context", {})
                for ctx_id, ctx_content in retrieved_context.items():
                    metadata = ctx_content.get("metadata", {})
                    text = sanitize_text(ctx_content.get("text", "N/A"))

                    # Write the entry row
                    context_ws.cell(row=context_current_row, column=1, value=sanitize_text(ctx_id))  # ContextID
                    context_ws.cell(row=context_current_row, column=2, value=sanitize_text(metadata.get("page_number", "N/A")))
                    context_ws.cell(row=context_current_row, column=3, value=sanitize_text(metadata.get("doc_title", "N/A")))
                    keywords = metadata.get("keywords", [])
                    keywords_sanitized = ', '.join([sanitize_text(k) for k in keywords]) if keywords else "N/A"
                    context_ws.cell(row=context_current_row, column=4, value=keywords_sanitized)
                    context_ws.cell(row=context_current_row, column=5, value=sanitize_text(metadata.get("information_category", "N/A")))
                    context_ws.cell(row=context_current_row, column=6, value=sanitize_text(metadata.get("source", "N/A")))
                    context_ws.cell(row=context_current_row, column=7, value=text)
                    context_ws.cell(row=context_current_row, column=7).alignment = Alignment(wrap_text=True)

                    # Apply alternating row colors for entries
                    if context_current_row % 2 == 0:
                        fill_color = "FFF2F2F2"  # Light Gray for even rows
                    else:
                        fill_color = "FFFFFFFF"  # White for odd rows
                    for col in range(1, 8):
                        context_ws.cell(row=context_current_row, column=col).fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")

                    # Record the cell address for this context ID (pointing to the 'ContextID' column)
                    cell_address = f"{get_column_letter(1)}{context_current_row}"  # Column 1 is 'ContextID'
                    context_links[(information_category, str(ctx_id))] = cell_address

                    context_current_row +=1

                # Add spacing after each section
                context_current_row +=1

            elif context_file:
                print(f"Context JSON file '{context_path}' for main file '{main_file}' does not exist. Skipping context data.")
            else:
                # Main file has no corresponding context JSON file
                continue

        # ----------------------------
        # 2. Process Patient Data
        # ----------------------------

        # Initialize row for Patient Data Sheet
        patient_current_row = 1
        feedback_headers_written = False

        for main_file, context_file in main_to_context_files.items():
            if main_file == f'{i}_treatment_summary.json':
                # Already processed in Treatment Summary sheet
                continue

            main_path = os.path.join(patient_dir, main_file)

            if not os.path.exists(main_path):
                print(f"Main JSON file '{main_path}' does not exist. Skipping.")
                continue

            with open(main_path, 'r') as mf:
                main_json = json.load(mf)

            # Extract information_category from main file name
            # For example, '0_treatment_summary.json' -> 'Treatment Summary'
            information_category = main_file.replace(f'{i}_', '').replace('.json', '').replace('_', ' ').strip().title()

            # Get color for main section
            main_color = main_section_colors.get(information_category, "FFD3D3D3")  # Default to Light Gray

            # Write section header for main category
            patient_current_row = write_patient_section(patient_ws, information_category, main_color, patient_current_row)

            # Depending on the main_file, process accordingly
            if main_file == f'{i}_Already experienced symptoms or side effects.json':
                # Processing 'Already experienced symptoms or side effects.json'

                question = "Already experienced symptoms or side effects of the patient and which drugs might have caused it?"
                answer = main_json.get(question, "N/A")

                current_section = "Already Experienced Symptoms or Side Effects"
                patient_current_row = write_patient_subsection_with_feedback(patient_ws, current_section, patient_current_row)

                patient_ws.cell(row=patient_current_row, column=1, value=sanitize_text(question))
                patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(answer))
                patient_current_row +=1

                # Leave feedback columns empty for user input
                patient_current_row +=1  # Blank row after section

            elif main_file == f'{i}_Cancer surveillance and other recommended tests for cancer monitoring.json':
                # Processing 'Cancer surveillance and other recommended tests for cancer monitoring.json'
                tests = main_json.get("Cancer surveillance and other recommended tests for cancer monitoring", [])
                if tests and isinstance(tests, list):
                    current_section = "Cancer Surveillance and Monitoring"
                    patient_current_row = write_patient_subsection_with_feedback(patient_ws, current_section, patient_current_row)

                    for test in tests:
                        patient_ws.cell(row=patient_current_row, column=1, value="Test Type")
                        test_type = test.get("Test type", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(test_type))
                        patient_current_row +=1

                        patient_ws.cell(row=patient_current_row, column=1, value="When / How Often")
                        when_how_often = test.get("When / how often", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(when_how_often))
                        patient_current_row +=1

                        patient_ws.cell(row=patient_current_row, column=1, value="Frequency (in weeks)")
                        frequency = test.get("Frequency (in weeks)", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(frequency) if frequency else "N/A")
                        patient_current_row +=1

                        patient_ws.cell(row=patient_current_row, column=1, value="Explanation")
                        explanation = test.get("Explanation", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(explanation))
                        patient_ws.cell(row=patient_current_row, column=2).alignment = Alignment(wrap_text=True)
                        patient_current_row +=1

                        patient_ws.cell(row=patient_current_row, column=1, value="Retrieved Context ID")
                        retrieved_id = test.get("Retrieved context id", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(retrieved_id))

                        # Create hyperlink to Context Data Sheet if context_id exists
                        context_key = ("cancer surveillance and other recommended tests for cancer monitoring", str(retrieved_id))
                        if context_key in context_links:
                            link_cell = context_links[context_key]
                            patient_ws.cell(row=patient_current_row, column=2).hyperlink = f"#'{context_sheet_name}'!{link_cell}"
                            patient_ws.cell(row=patient_current_row, column=2).font = Font(color="0000FF", underline="single")
                        else:
                            print(f"Context ID '{retrieved_id}' not found in Context Data Sheet for Patient {i}.")

                        # Apply alternating row colors
                        if patient_current_row % 2 == 0:
                            fill_color = "FFF2F2F2"  # Light Gray for even rows
                        else:
                            fill_color = "FFFFFFFF"  # White for odd rows
                        for col in range(1,7):
                            patient_ws.cell(row=patient_current_row, column=col).fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")

                        patient_current_row +=1

                        # Leave feedback columns empty for user input
                        patient_current_row +=1  # Blank row after each test
                else:
                    print(f"No cancer surveillance data found in '{main_file}' for Patient {i}.")

            elif main_file == f'{i}_Lifestyle and behavior recommendations for cancer survivors.json':
                # Processing 'Lifestyle and behavior recommendations for cancer survivors.json'
                recommendations = main_json.get("Lifestyle and behavior recommendations for cancer survivors", [])
                if recommendations and isinstance(recommendations, list):
                    current_section = "Lifestyle and Behavior Recommendations"
                    patient_current_row = write_patient_subsection_with_feedback(patient_ws, current_section, patient_current_row)

                    for rec in recommendations:
                        patient_ws.cell(row=patient_current_row, column=1, value="Lifestyle")
                        lifestyle = rec.get("Lifestyle", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(lifestyle))
                        patient_current_row +=1

                        patient_ws.cell(row=patient_current_row, column=1, value="Explanation")
                        explanation = rec.get("Explanation", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(explanation))
                        patient_ws.cell(row=patient_current_row, column=2).alignment = Alignment(wrap_text=True)
                        patient_current_row +=1

                        patient_ws.cell(row=patient_current_row, column=1, value="Retrieved Context ID")
                        retrieved_id = rec.get("Retrieved context id", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(retrieved_id))

                        # Create hyperlink to Context Data Sheet if context_id exists
                        context_key = ("lifestyle and behavior recommendations for cancer survivors", str(retrieved_id))
                        if context_key in context_links:
                            link_cell = context_links[context_key]
                            patient_ws.cell(row=patient_current_row, column=2).hyperlink = f"#'{context_sheet_name}'!{link_cell}"
                            patient_ws.cell(row=patient_current_row, column=2).font = Font(color="0000FF", underline="single")
                        else:
                            print(f"Context ID '{retrieved_id}' not found in Context Data Sheet for Patient {i}.")

                        # Apply alternating row colors
                        if patient_current_row % 2 == 0:
                            fill_color = "FFF2F2F2"  # Light Gray for even rows
                        else:
                            fill_color = "FFFFFFFF"  # White for odd rows
                        for col in range(1,7):
                            patient_ws.cell(row=patient_current_row, column=col).fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")

                        patient_current_row +=1

                        # Leave feedback columns empty for user input
                        patient_current_row +=1  # Blank row after each recommendation
                else:
                    print(f"No lifestyle and behavior recommendations found in '{main_file}' for Patient {i}.")

            elif main_file == f'{i}_Possible late and long-term effects of cancer treatment.json':
                # Processing 'Possible late and long-term effects of cancer treatment.json'
                effects = main_json.get("Possible late and long-term effects of cancer treatment", [])
                if effects and isinstance(effects, list):
                    current_section = "Possible Late and Long-term Effects of Cancer Treatment"
                    patient_current_row = write_patient_subsection_with_feedback(patient_ws, current_section, patient_current_row)

                    for effect in effects:
                        patient_ws.cell(row=patient_current_row, column=1, value="Treatment Effect")
                        treatment_effect = effect.get("Treatment effect", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(treatment_effect))
                        patient_current_row +=1

                        patient_ws.cell(row=patient_current_row, column=1, value="Explanation")
                        explanation = effect.get("Explanation", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(explanation))
                        patient_ws.cell(row=patient_current_row, column=2).alignment = Alignment(wrap_text=True)
                        current_row +=1

                        patient_ws.cell(row=patient_current_row, column=1, value="Retrieved Context ID")
                        retrieved_id = effect.get("Retrieved context id", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(retrieved_id))

                        # Create hyperlink to Context Data Sheet if context_id exists
                        context_key = ("possible late and long-term effects of cancer treatment", str(retrieved_id))
                        if context_key in context_links:
                            link_cell = context_links[context_key]
                            patient_ws.cell(row=patient_current_row, column=2).hyperlink = f"#'{context_sheet_name}'!{link_cell}"
                            patient_ws.cell(row=patient_current_row, column=2).font = Font(color="0000FF", underline="single")
                        else:
                            print(f"Context ID '{retrieved_id}' not found in Context Data Sheet for Patient {i}.")

                        # Apply alternating row colors
                        if patient_current_row % 2 == 0:
                            fill_color = "FFF2F2F2"  # Light Gray for even rows
                        else:
                            fill_color = "FFFFFFFF"  # White for odd rows
                        for col in range(1,7):
                            patient_ws.cell(row=patient_current_row, column=col).fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")

                        patient_current_row +=1

                        # Leave feedback columns empty for user input
                        patient_current_row +=1  # Blank row after each effect
                else:
                    print(f"No late and long-term effects data found in '{main_file}' for Patient {i}.")

            elif main_file == f'{i}_Possible other issues that cancer survivors may experience.json':
                # Processing 'Possible other issues that cancer survivors may experience.json'
                issues = main_json.get("Possible other issues that cancer survivors may experience", [])
                if issues and isinstance(issues, list):
                    current_section = "Possible Other Issues"
                    patient_current_row = write_patient_subsection_with_feedback(patient_ws, current_section, patient_current_row)

                    for issue in issues:
                        patient_ws.cell(row=patient_current_row, column=1, value="Issue")
                        issue_desc = issue.get("Issue", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(issue_desc))
                        patient_current_row +=1

                        patient_ws.cell(row=patient_current_row, column=1, value="Explanation")
                        explanation = issue.get("Explanation", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(explanation))
                        patient_ws.cell(row=patient_current_row, column=2).alignment = Alignment(wrap_text=True)
                        current_row +=1

                        patient_ws.cell(row=patient_current_row, column=1, value="Retrieved Context ID")
                        retrieved_id = issue.get("Retrieved context id", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(retrieved_id))

                        # Create hyperlink to Context Data Sheet if context_id exists
                        context_key = ("possible other issues that cancer survivors may experience", str(retrieved_id))
                        if context_key in context_links:
                            link_cell = context_links[context_key]
                            patient_ws.cell(row=patient_current_row, column=2).hyperlink = f"#'{context_sheet_name}'!{link_cell}"
                            patient_ws.cell(row=patient_current_row, column=2).font = Font(color="0000FF", underline="single")
                        else:
                            print(f"Context ID '{retrieved_id}' not found in Context Data Sheet for Patient {i}.")

                        # Apply alternating row colors
                        if patient_current_row % 2 == 0:
                            fill_color = "FFF2F2F2"  # Light Gray for even rows
                        else:
                            fill_color = "FFFFFFFF"  # White for odd rows
                        for col in range(1,7):
                            patient_ws.cell(row=patient_current_row, column=col).fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")

                        patient_current_row +=1

                        # Leave feedback columns empty for user input
                        patient_current_row +=1  # Blank row after each issue
                else:
                    print(f"No other issues data found in '{main_file}' for Patient {i}.")

            elif main_file == f'{i}_References to helpful resources for cancer survivors.json':
                # Processing 'References to helpful resources for cancer survivors.json'
                references = main_json.get("References to helpful resources for cancer survivors", [])
                if references and isinstance(references, list):
                    current_section = "References to Helpful Resources"
                    patient_current_row = write_patient_subsection_with_feedback(patient_ws, current_section, patient_current_row)

                    for ref in references:
                        patient_ws.cell(row=patient_current_row, column=1, value="Resource")
                        resource = ref.get("Resource", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(resource))
                        patient_current_row +=1

                        patient_ws.cell(row=patient_current_row, column=1, value="Explanation")
                        explanation = ref.get("Explanation", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(explanation))
                        patient_ws.cell(row=patient_current_row, column=2).alignment = Alignment(wrap_text=True)
                        current_row +=1

                        patient_ws.cell(row=patient_current_row, column=1, value="Retrieved Context ID")
                        retrieved_id = ref.get("Retrieved context id", "N/A")
                        patient_ws.cell(row=patient_current_row, column=2, value=sanitize_text(retrieved_id))

                        # Create hyperlink to Context Data Sheet if context_id exists
                        context_key = ("references to helpful resources for cancer survivors", str(retrieved_id))
                        if context_key in context_links:
                            link_cell = context_links[context_key]
                            patient_ws.cell(row=patient_current_row, column=2).hyperlink = f"#'{context_sheet_name}'!{link_cell}"
                            patient_ws.cell(row=patient_current_row, column=2).font = Font(color="0000FF", underline="single")
                        else:
                            print(f"Context ID '{retrieved_id}' not found in Context Data Sheet for Patient {i}.")

                        # Apply alternating row colors
                        if patient_current_row % 2 == 0:
                            fill_color = "FFF2F2F2"  # Light Gray for even rows
                        else:
                            fill_color = "FFFFFFFF"  # White for odd rows
                        for col in range(1,7):
                            patient_ws.cell(row=patient_current_row, column=col).fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")

                        patient_current_row +=1

                        # Leave feedback columns empty for user input
                        patient_current_row +=1  # Blank row after each reference
                else:
                    print(f"No references data found in '{main_file}' for Patient {i}.")

            else:
                print(f"Unrecognized main JSON file '{main_file}' for Patient {i}. Skipping.")

            # Add an extra blank row after each main section
            patient_current_row +=1

        # ----------------------------
        # 4. Add Overall Feedback in Patient Data Sheet
        # ----------------------------

        overall_feedback_start_row = patient_current_row +1  # Add an empty row before overall feedback
        overall_feedback_start_row = write_patient_subsection_with_feedback(patient_ws, "Overall Feedback", overall_feedback_start_row)

        # Define overall feedback questions
        overall_feedback_questions = [
            "Is this customized to the patients' needs (0-5)",
            "Clarity and understandability (0-5)",
            "Comprehensiveness (0-5)",
            "Comments"
        ]

        for question in overall_feedback_questions:
            patient_ws.cell(row=overall_feedback_start_row, column=1, value=question)
            if question != "Comments":
                patient_ws.cell(row=overall_feedback_start_row, column=2, value="")
            else:
                patient_ws.cell(row=overall_feedback_start_row, column=2, value="")
            # Apply formatting
            patient_ws.cell(row=overall_feedback_start_row, column=1).font = Font(bold=True)
            patient_ws.cell(row=overall_feedback_start_row, column=1).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
            # Apply alternating row colors
            if overall_feedback_start_row % 2 == 0:
                fill_color = "FFF2F2F2"  # Light Gray
            else:
                fill_color = "FFFFFFFF"  # White
            for col in range(1,7):
                patient_ws.cell(row=overall_feedback_start_row, column=col).fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
            overall_feedback_start_row +=1

        # Adjust column widths for Patient Data sheet
        adjust_column_widths(patient_ws)

    # ----------------------------
    # 5. Final Formatting
    # ----------------------------

    # Adjust column widths for all sheets
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        adjust_column_widths(ws)

    # Set alignment for all cells
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        for row in ws.iter_rows():
            for cell in row:
                if cell.value:
                    cell.alignment = Alignment(wrap_text=True, vertical='top')

    # ----------------------------
    # 6. Save the Workbook
    # ----------------------------

    output_file = "Patients_Data_Summary.xlsx"
    wb.save(output_file)

    print(f"Excel file '{output_file}' has been created successfully.")
