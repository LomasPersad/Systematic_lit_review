from nltk.tokenize import sent_tokenize
import pdfplumber
import re
# import nltk

# nltk.download("punkt")


def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text


def summarize_methodology(text):
    # Split the text into sentences
    sentences = sent_tokenize(text)
    # Look for the start and end of the methodology section
    methodology_start = None
    methodology_end = None

    for i, sentence in enumerate(sentences):
        # You can customize this logic based on common phrases or keywords
        if "methodology" in sentence.lower() or "methods" in sentence.lower():
            methodology_start = i
            break

    if methodology_start is not None:
        # Assume the methodology section ends when a new section begins
        for i in range(methodology_start + 1, len(sentences)):
            if sentences[i].strip() == "RESULTS":
                methodology_end = i
                break

        # Summarize the methodology section
        print(methodology_start)
        print(methodology_end)
        if methodology_end is not None:
            methodology_summary = " ".join(
                sentences[methodology_start:methodology_end])
            return methodology_summary

    return "Methodology section not found."


# Replace 'your_paper.pdf' with the path to your research paper PDF
pdf_path = 'examplePaper.pdf'
# text = extract_text_from_pdf(pdf_path)
# methodology_summary = summarize_methodology(text)

# print("Methodology Summary:")
# print(methodology_summary)


def extract_methodology_re(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    # Define keywords or patterns to identify methodology headings
    methodology_keywords = ["Methodology",
                            "Materials and Methods", "Experimental Procedure", "Methods"]

    # Split the text into sections based on headings
    sections = re.split(r'(\n[^\n]*\n)', text)
    print(sections[2])

    # Search for the methodology section
    methodology_section = ""
    in_methodology = False
    for section in sections:
        section = section.strip()
        if any(keyword in section for keyword in methodology_keywords):
            in_methodology = True

        elif in_methodology and section:
            # Append the text to the methodology section
            methodology_section += section + "\n"

    return methodology_section

# Replace 'your_paper.pdf' with the path to your research paper PDF


# methodology_text = extract_methodology(pdf_path)

# Print the methodology section
# print("Methodology Section:")
# print(methodology_text)

def extract_methodology(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            left = page.crop((0, 0, 0.5 * page.width, 0.9 * page.height))
            right = page.crop((0.5 * page.width, 0, page.width, page.height))
            l_text = left.extract_text()
            r_text = right.extract_text()
            text += l_text + " " + r_text
            # text += page.extract_text()

    # Define a regular expression pattern to match the METHODS section
    pattern = r'(?i)METHODS|METHODOLOGY'

    # Use re.search to find the start of the METHODS section
    match = re.search(pattern, text)

    if match:
        start_index = match.start()
        # Find the end of the METHODS section
        end_index = text.find("RESULTS", start_index)

        if end_index == -1:
            # If "RESULTS" is not found, assume the end of the document
            end_index = len(text)

        # Extract the METHODS section
        methodology_section = text[start_index:end_index]
        return methodology_section

    return None


methodology_text = extract_methodology(pdf_path)

if methodology_text:
    # Print the methodology section
    print("Methodology Section:")
    print(methodology_text)
else:
    print("METHODS section not found in the document.")
