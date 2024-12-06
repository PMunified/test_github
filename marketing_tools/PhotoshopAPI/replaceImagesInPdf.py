import fitz  # PyMuPDF
from fpdf import FPDF

def replace_images_in_pdf(input_pdf_path, output_pdf_path, new_image_path, page_number):
    # Open the source PDF
    pdf_document = fitz.open(input_pdf_path)
    page = pdf_document[page_number]

    # Extract the size of the page
    page_width, page_height = page.rect.width, page.rect.height

    # Convert from points to mm (FPDF uses mm by default)
    page_width_mm = page_width * 0.352778
    page_height_mm = page_height * 0.352778

    # Extract the image rectangles
    image_rects = []
    for img in page.get_images(full=True):
        xref = img[0]
        rect = page.get_image_rects(xref)[0]
        image_rects.append(rect)

    # Create a new PDF with fpdf, setting the size to match the original PDF
    pdf_writer = FPDF(unit='mm', format=(page_width_mm, page_height_mm))
    pdf_writer.add_page()

    # Add the new image(s) in place of the old images
    for rect in image_rects:
        # Convert the coordinates and dimensions from points to mm
        x = rect.x0 * 0.352778
        y = rect.y0 * 0.352778
        w = rect.width * 0.352778
        h = rect.height * 0.352778

        # Add the new image to the PDF
        pdf_writer.image(new_image_path, x=x, y=y, w=w, h=h)

    # Save the new PDF
    pdf_writer.output(output_pdf_path)

# Example usage
input_pdf = 'C:/python_workspace/NEWITEMS/marketing_tools/jan24_eng.pdf'
output_pdf = 'C:/python_workspace/NEWITEMS/marketing_tools/output2.pdf'
new_image = 'C:/python_workspace/NEWITEMS/marketing_tools/new_image1.jpg'
replace_images_in_pdf(input_pdf, output_pdf, new_image, page_number=2)  # Replace images on the first page
