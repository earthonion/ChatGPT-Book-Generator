import os
import openai
import json
import time
import config
import re
from fpdf import FPDF

openai.api_key = config.OPENAI_KEY

def sanitize_filename(filename):
    """Sanitizes the given filename by replacing any non-alphanumeric character with an underscore."""
    return re.sub(r'[^\w\-_]', '_', filename)

def gen_pdf(book_title, book_json):
    """Generates a PDF file for the given book title and JSON content."""
    # Define various font sizes and styles
    chapter_title_font_size = 24
    subchapter_title_font_size = 20
    section_title_font_size = 16
    content_font_size = 12
    chapter_title_style = 'B'

    # Create PDF with defined parameters
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_margins(left=10, top=10, right=10)

    # Add title page
    pdf.add_font('DejaVu', '', os.path.abspath('/Library/Fonts/DejaVuSans.ttf'), uni=True)
    pdf.set_font('DejaVu', style=chapter_title_style, size=36)
    pdf.multi_cell(w=0, h=20, txt=book_title, align='C')
    pdf.add_page()

    # Iterate through chapters and add content to PDF
    for chapter in book_json:
        # Set chapter title font and size
        pdf.set_font('DejaVu', style=chapter_title_style, size=chapter_title_font_size)
        pdf.multi_cell(w=0, h=15, txt=chapter['chapter_title'], align='C')

        for subchapter in chapter['subchapters']:  # Iterate through subchapters
            # Set subchapter title font and size
            pdf.set_font('DejaVu', style='', size=subchapter_title_font_size)
            pdf.multi_cell(w=0, h=12, txt=subchapter['subchapter_title'], align='L')

            for section in subchapter['sections']:  # Access sections inside subchapter
                # Set section font and size
                pdf.set_font('DejaVu', style='', size=section_title_font_size)
                pdf.cell(w=0, h=15, txt=section['section'], ln=1, align='L')

                # Set content font and size
                pdf.set_font('DejaVu', style='', size=content_font_size)
                pdf.multi_cell(w=0, h=10, txt=section['content'], align='J')

        # Add a new page for next chapter
        pdf.add_page()

    # Generate sanitized filename and output the PDF file
    book_out = sanitize_filename(book_title) + '.pdf'
    pdf.output(book_out, 'F')
    print(book_out)

def print_progress_bar(chapter_name, subchapter_name, section_name, completion_percentage):
    """Prints a progress bar for the given chapter, subchapter, section, and completion percentage."""
    bar_length = 50
    progress = int(bar_length * completion_percentage)
    print(f"Chapter: {chapter_name}\nsubchapter: {subchapter_name}\nsection: {section_name}\n[{'#' * progress}{'-' * (bar_length - progress)}] {int(completion_percentage * 100)}%", end='\r\n')

def save(filename, text):
    """Saves the given text to a file with the specified filename."""
    with open(filename, 'w+') as f:
        f.write(text)

def call_with_retry(func, *args, max_retries=5, retry_delay=60):
    """Calls the specified function with the given arguments, retrying up to max_retries times if a RateLimitError is encountered."""
    retries = 0
    while retries <= max_retries:
        try:
            return func(*args)
        except openai.error.RateLimitError:
            print(f'Rate limit reached. Retrying in {retry_delay} seconds...')
            time.sleep(retry_delay)
            retries += 1
            retry_delay *= 2  # Exponential backoff
        except openai.error.OpenAIError as e:
            print(f'An error occurred with OpenAI: {e}. Retrying...')
            retries += 1
    raise Exception('Max retries reached')

def generate_chapters(book_title):
    """Generates chapters for a given book title, requesting input from OpenAI's model."""
    def api_call():
        prompt = [
            {"role": "system", "content": f"You are writing a book titled {book_title}. Please create an organized list of chapters and sections in the following format: {json.dumps({'chapter_name': ['section_names']})}. Include 5 to 10 sections for each chapter. Keep the structure clear and coherent."},
            {"role": "user", "content": "Sure, let's create an engaging and well-structured outline for the readers."}
        ]
        return openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", messages=prompt)['choices'][0]['message']['content']

    return call_with_retry(api_call)

def generate_content(chapter_name, section_name, book_title):
    """Generates content for a given chapter and section, requesting input from OpenAI's model."""
    def api_call():
        prompt = [
            {"role": "system", "content": f"You are writing content for the book titled '{book_title}', specifically for chapter '{chapter_name}' and section '{section_name}'. Please provide engaging, insightful, and varied content for this section. The length of subchapters, paragraphs, and sentences should differ to create a dynamic reading experience. Avoid repetition and monotony, and make sure to keep the reader's interest throughout."},
            {"role": "user", "content": "Certainly! Let's explore this section with a fresh perspective, varying the structure and style to engage the reader."}
        ]
        return openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", messages=prompt)['choices'][0]['message']['content']

    return call_with_retry(api_call)

if __name__ == '__main__':
    # Check if chapters file already exists
    chapters_file = 'chapters.json'
    if os.path.exists(chapters_file):
        with open(chapters_file, 'r') as file:
            chapters_names = file.read()
        # Extract the book title from the existing chapters
        book_title = list(json.loads(chapters_names).keys())[0].split(':')[0]
    else:
        # If chapters file does not exist, prompt for a book title and generate the chapters
        book_title = input("please input a book title: ")
        chapters_names = generate_chapters(book_title)
        save(chapters_file, chapters_names)

    # Convert the chapter names to JSON
    chapters_json = json.loads(chapters_names)
    total_chapters = len(chapters_json)
    chapters = []

    # Iterate through the chapters, subchapters, and sections
    for chapter_index, (chapter_name, subchapters_dict) in enumerate(list(chapters_json.items())):
        total_subchapters = len(subchapters_dict)
        all_subchapters = []

        for subchapter_index, (subchapter_name, sections) in enumerate(list(subchapters_dict.items())):
            total_sections = len(sections)
            subchapters = []

            for section_index, section_name in enumerate(sections):
                # Compute and print the completion percentage
                completion_percentage = (chapter_index + (subchapter_index / total_subchapters) + (section_index / (total_sections * total_subchapters))) / total_chapters
                print_progress_bar(chapter_name, subchapter_name, section_name, completion_percentage)

                while True:
                    try:
                        # Generate content for each section
                        content = generate_content(chapter_name, section_name, book_title)
                        break
                    except openai.error.RateLimitError:
                        print('Ratelimit Trying again in 5 minutes')
                        time.sleep(5 * 60)

                subchapter = {
                    "section": section_name,
                    "content": content
                }
                subchapters.append(subchapter)

            all_subchapters.append({
                "subchapter_title": subchapter_name,
                "sections": subchapters
            })

        # Add chapter to the chapters list
        chapter = {
            "chapter_title": chapter_name,
            "subchapters": all_subchapters
        }
        chapters.append(chapter)

    # Save the chapters as JSON
    book_out = sanitize_filename(book_title) + '.json'
    save(book_out, json.dumps(chapters, indent=4).replace('\u2019', '\'').replace('\u201c', '\"').replace('\u2013', '\"').replace('\u201d', '\"'))

    # Generate the PDF file
    gen_pdf(book_title, chapters)
