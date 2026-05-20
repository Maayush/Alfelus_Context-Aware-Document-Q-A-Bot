from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):

    text = ""

    try:

        reader = PdfReader(pdf_path)

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    except Exception as e:

        print("PDF Error:", str(e))

        return ""

    return text