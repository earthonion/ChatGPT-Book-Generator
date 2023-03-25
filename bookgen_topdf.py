import json
from fpdf import FPDF


def gen_pdf(book_title, book_json):
    # Define the font sizes and styles
    chapter_title_font_size = 24
    subchapter_title_font_size = 16
    content_font_size = 12
    chapter_title_style = 'B'

    # Create a new PDF object with UTF-8 encoding
    pdf = FPDF(orientation='P', unit='mm', format='A4')

# Set the page dimensions and margins
    pdf.add_page()
    pdf.set_margins(left=10, top=10, right=10)

# Write the book title and chapters to the PDF
    pdf.set_font(family='Arial',         style=chapter_title_style, size=36)
    
    pdf.multi_cell(w=0, h=20, txt=book_title,  align='C')
    pdf.add_page()
# Loop through the chapters and subchapters
    for chapter in book_json:
    # Write the chapter title
        pdf.set_font(family='Arial', style=chapter_title_style, size=chapter_title_font_size)
        pdf.multi_cell(w=0, h=15, txt=chapter['chapter_title'],  align='C')

    # Loop through the subchapters
        for subchapter in chapter['subchapters']:
        # Write the subchapter title
            pdf.set_font(family='Arial', style='', size=subchapter_title_font_size)
            pdf.cell(w=0, h=15, txt=subchapter['subchapter'], ln=1, align='L')

        # Write the subchapter content
            pdf.set_font(family='Arial', style='', size=content_font_size)
            pdf.multi_cell(w=0, h=10, txt=subchapter['content'], align='J')

    # Add a new page after each chapter
        pdf.add_page()

# Save the PDF file
    book_out = book_title.replace(' ', '_').replace(':','-').replace('?','')+ '.pdf'
    pdf.output(book_out, 'F')
    print(book_out)
