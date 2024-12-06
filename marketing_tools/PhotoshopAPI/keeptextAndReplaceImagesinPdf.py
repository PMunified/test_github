import fitz  # PyMuPDF
from fpdf import FPDF
'''
def extract_text_and_images(input_pdf_path, page_number):
    # Open the PDF
    pdf_document = fitz.open(input_pdf_path)
    page = pdf_document.load_page(page_number)

    # Extract text
    text = page.get_text()

    # Extract images
    images = []
    for img in page.get_images(full=True):
        xref = img[0]
        rect = page.get_image_rects(xref)[0]
        images.append((xref, rect))

    # Extract page dimensions in points
    page_width, page_height = page.rect.width, page.rect.height

    return text, images, page_width, page_height

def create_pdf_with_replacement(text, images, new_image_path, output_pdf_path, page_width, page_height):
    # Convert points to millimeters
    pt_to_mm = 0.352778
    page_width_mm = page_width * pt_to_mm
    page_height_mm = page_height * pt_to_mm

    # Create a new PDF with fpdf
    pdf_writer = FPDF(unit='mm', format=(page_width_mm, page_height_mm))
    pdf_writer.add_page()

    # Add original text to the new PDF
    pdf_writer.set_font("Arial", size=12)
    pdf_writer.set_xy(10, 10)  # Start at a position
    pdf_writer.multi_cell(0, 10, text)  # Adjust font size if needed

    # Add the new image(s) in place of the old images
    for xref, rect in images:
        x = rect.x0 * pt_to_mm
        y = rect.y0 * pt_to_mm
        w = rect.width * pt_to_mm
        h = rect.height * pt_to_mm
        
        # Add the new image to the PDF
        pdf_writer.image(new_image_path, x=x, y=y, w=w, h=h)

    # Save the new PDF
    pdf_writer.output(output_pdf_path)
'''    
def extract_text_and_images(input_pdf_path, page_number):
    # Open the PDF
    pdf_document = fitz.open(input_pdf_path)
    page = pdf_document.load_page(page_number)

    # Extract text with positions
    text_blocks = page.get_text("dict")["blocks"]

    # Extract images
    images = []
    for img in page.get_images(full=True):
        xref = img[0]
        rect = page.get_image_rects(xref)[0]
        images.append((xref, rect))

    # Extract page dimensions in points
    page_width, page_height = page.rect.width, page.rect.height

    return text_blocks, images, page_width, page_height


def create_pdf_with_replacement(text_blocks, images, new_image_path, output_pdf_path, page_width, page_height):
    # Convert points to millimeters
    pt_to_mm = 0.352778
    page_width_mm = page_width * pt_to_mm
    page_height_mm = page_height * pt_to_mm

    # Create a new PDF with FPDF
    pdf_writer = FPDF(unit='mm', format=(page_width_mm, page_height_mm))
    pdf_writer.add_page()

    # Disable automatic page breaks to avoid creating extra pages
    pdf_writer.set_auto_page_break(auto=False)

    # Add original text to the new PDF with correct positioning
    pdf_writer.set_font("Arial", size=10)

    for block in text_blocks:
        if block["type"] == 0:  # Text block
            for line in block["lines"]:
                for span in line["spans"]:
                    # Extract font size
                    font_size = span["size"] * pt_to_mm

                    # Convert coordinates from points to mm
                    x = span["bbox"][0] * pt_to_mm
                    text_height = (span["bbox"][3] - span["bbox"][1]) * pt_to_mm  # Height of text box

                    # Flip Y-axis by subtracting from page_height
                    y = (page_height - span["bbox"][1]) * pt_to_mm - text_height

                    # Debug: Print each text span's original and converted coordinates
                    print(f"Original text coordinates: x={span['bbox'][0]}, y={span['bbox'][1]}")
                    print(f"Converted text coordinates: x={x}, y={y}")

                    # Set the font size
                    pdf_writer.set_font_size(font_size)

                    # Set position and write the text
                    pdf_writer.set_xy(x, y)
                    pdf_writer.cell(0, text_height, span["text"], ln=False)  # Avoid line breaks with ln=False

    # Add the new image(s) in place of the old images
    for xref, rect in images:
        x = rect.x0 * pt_to_mm
        # Flip Y-axis for image by subtracting Y0 from page_height and adjusting for image height
        y = (page_height - rect.y0) * pt_to_mm - (rect.height * pt_to_mm)
        w = rect.width * pt_to_mm
        h = rect.height * pt_to_mm

        # Debug: Print each image's original and converted coordinates
        print(f"Original image coordinates: x0={rect.x0}, y0={rect.y0}, x1={rect.x1}, y1={rect.y1}")
        print(f"Converted image coordinates: x={x}, y={y}, width={w}, height={h}")

        # Add the new image to the PDF
        pdf_writer.image(new_image_path, x=x, y=y, w=w, h=h)

    # Save the new PDF
    pdf_writer.output(output_pdf_path)
    
# Example usage
input_pdf = 'C:/python_workspace/NEWITEMS/marketing_tools/jan24_eng.pdf'
output_pdf = 'C:/python_workspace/NEWITEMS/marketing_tools/output2.pdf'
new_image = 'C:/python_workspace/NEWITEMS/marketing_tools/new_image1.jpg'

# Extract text and image positions from the input PDF
text, images, page_width, page_height = extract_text_and_images(input_pdf, page_number=2)

# Create a new PDF with the extracted text and new images
create_pdf_with_replacement(text, images, new_image, output_pdf, page_width, page_height)
