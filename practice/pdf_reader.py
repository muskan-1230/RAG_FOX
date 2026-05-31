from pypdf import PdfReader

pdf_path = "sample.pdf"

reader = PdfReader(pdf_path)

print(f"Total Pages: {len(reader.pages)}")

text = ""

for page in reader.pages:
    text += page.extract_text() + "\n"

print("\n===== PDF CONTENT =====\n")
print(text)