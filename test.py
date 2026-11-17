from pypdf import PdfReader

reader = PdfReader("documents/FAQ.pdf")

for page_num, page in enumerate(reader.pages):
    print(f"\n--- PAGE {page_num + 1} ---")
    print(page.extract_text())