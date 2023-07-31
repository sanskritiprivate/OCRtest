import re
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import AnnotationBuilder


t1_start_date = datetime(2022, 8, 30)
t1_end_date = datetime(2022, 11, 4)
t2_start_date = datetime(2022, 11, 7)
t2_end_date = datetime(2023, 1, 27)
t3_start_date = datetime(2023, 1, 30)
t3_end_date = datetime(2023, 4, 7)
t4_start_date = datetime(2023, 4, 10)
t4_end_date = datetime(2023, 6, 12)


pdfs = []


def annotate(counter, page, grade, term):
    page = page
    writer = PdfWriter()
    writer.add_page(page)

    annotation = AnnotationBuilder.free_text(
        "Grade: {}\nTerm: {}".format(grade, term),
        rect=(0, 0, 35, 250),
        font="Arial",
        bold=True,
        italic=True,
        font_size="20pt",
        font_color="00ff00",
        border_color="0000ff",
        background_color="cdcdcd",
    )
    writer.add_annotation(page_number=0, annotation=annotation)

    # Write the annotated file to disk
    with open("attendance{}.pdf".format(str(counter)), "wb") as fp:
        writer.write(fp)
    pdfs.append("attendance{}.pdf".format(str(counter)))



def find_term(start_date, end_date):
    # print(start_date, end_date)
    if start_date >= t1_start_date and end_date <= t1_end_date:
        return "Term 1"
    elif start_date >= t2_start_date and end_date <= t2_end_date:
        return "Term 2"
    elif start_date >= t3_start_date and end_date <= t3_end_date:
        return "Term 3"
    elif start_date >= t4_start_date and end_date <= t4_end_date:
        return "Term 4"


def extract_term(text):
    from_match = re.search("From:", text)
    to_match = re.search("To:", text)

    term_start_index = from_match.end() + 1
    term_start_index2 = from_match.end() + 11
    term_end_index = to_match.end() + 1
    term_end_index2 = to_match.end() + 11

    start_date = datetime.strptime(text[term_start_index:term_start_index2], '%m/%d/%Y')
    end_date = datetime.strptime(text[term_end_index:term_end_index2], '%m/%d/%Y')

    term = find_term(start_date, end_date)
    return term

if __name__ == '__main__':
    reader = PdfReader('/Users/sanskrititimseena/Downloads/attendance.pdf')
    all_texts = []
    counter = 0

    for page in reader.pages:
        # print(page.extract_text())
        text = page.extract_text()

        grade_match = re.search("Grade:", text)
        if grade_match:
            # find grade
            grade_start = grade_match.end() + 1
            grade_end = grade_match.end() + 3
            grade = text[grade_start:grade_end]

            term = extract_term(text)

        page.rotate(270)
        annotated_pdf = annotate(counter, page, grade, term)
        counter = counter + 1

        merger = PdfWriter()

        for pdf in pdfs:
            merger.append(pdf)

        merger.write("merged-pdf.pdf")
        merger.close()





