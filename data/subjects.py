from pathlib import Path

import openpyxl

FILE_PATH = Path(__file__).parent / "subjects_tusur_reduced.xlsx"


def load_subjects():
    workbook = openpyxl.load_workbook(FILE_PATH, read_only=True)
    sheet = workbook.active

    subjects = {}
    for name, rank, exam_type in sheet.iter_rows(min_row=2, values_only=True):
        if name is None:
            continue
        subjects[name] = {"rank": rank, "exam_type": exam_type}

    workbook.close()
    return subjects


SUBJECTS_DATA = load_subjects()
SUBJECTS = list(SUBJECTS_DATA.keys())