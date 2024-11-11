from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation

# Constants
FACES_PER_SHEET = 4
SHEETS_PER_BOOKLET = 4
FACES_PER_BOOKLET = FACES_PER_SHEET * SHEETS_PER_BOOKLET

# Input Files
input_reader = PdfReader("testing/dummy.pdf")
signature_reader = PdfReader("store/signature.pdf")
print(f"Input reader length: {len(input_reader.pages)}")
print(f"Signature reader length: {len(signature_reader.pages)}")

# Create initial PDF
writer = PdfWriter()
writer.append_pages_from_reader(input_reader)
writer.append_pages_from_reader(signature_reader)

remainder_pages = len(writer.pages) % FACES_PER_BOOKLET
end_blank_pages = FACES_PER_BOOKLET - remainder_pages
for a in range(end_blank_pages):
    writer.add_blank_page()

print(remainder_pages)
print(end_blank_pages)
print(len(writer.pages))


# for num, page in enumerate(writer.pages):
#     print(num, type(page))




# writer.add_page(reader.pages[0])
# writer.add_page(reader.pages[1])
# writer.pages[0].rotate(90)
# writer.pages[1].rotate(-90)

# writer.pages[0].merge_page(writer.rotate(90), expand=True)

big_page = PageObject.create_blank_page(height=writer.pages[0].mediabox.height, width=writer.pages[0].mediabox.width * 2) 

# big_page.merge_page(writer.pages[0])

# writer.pages[1].add_transformation(Transformation().translate(tx=writer.pages[0].mediabox.width))
translated_1 = writer.pages[1]
# translated_1.add_transformation(Transformation().translate(tx=writer.pages[0].mediabox.width))


big_page.merge_page(writer.pages[0])
# big_page.merge_page(writer.pages[1])

writer.add_page(big_page)



with open("testing/dummy_output.pdf", "wb") as fp:
    writer.write(fp)