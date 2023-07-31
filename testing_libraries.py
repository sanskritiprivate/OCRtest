from PyPDF2 import PdfReader
import re
from datetime import datetime


reader = PdfReader('/Users/sanskrititimseena/Downloads/attendance.pdf')

page = reader.pages[0]

text = page.extract_text()

from_match = re.search("from", text, re.IGNORECASE)
to_match = re.search("to", text, re.IGNORECASE)
grade_match = re.search("grade", text, re.IGNORECASE)
grade_start = grade_match.end() + 2
grade_end = grade_match.end() + 4
grade = text[grade_start:grade_end]
print(grade)

term_start_index = from_match.end() + 2
term_start_index2 = from_match.end() + 12
term_end_index = to_match.end() + 2
term_end_index2 = to_match.end() + 12

date = text[term_start_index:term_start_index2]
print(date)

print(datetime.strptime(date, '%m/%d/%Y'))



# add annotation to pdf
from pypdf import PdfReader, PdfWriter
from pypdf.generic import AnnotationBuilder

# Fill the writer with the pages you want
pdf_path = "/Users/sanskrititimseena/Downloads/attendance.pdf"
reader = PdfReader(pdf_path)
page = reader.pages[0]
writer = PdfWriter()
writer.add_page(page)

# Create the annotation and add it
annotation = AnnotationBuilder.free_text(
    "Grade: {}".format(grade),
    rect=(50, 550, 200, 650),
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
with open("annotated-pdf.pdf", "wb") as fp:
    writer.write(fp)



