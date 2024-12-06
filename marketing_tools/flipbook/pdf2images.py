from spire.pdf.common import *
from spire.pdf import *

# Create a PdfDocument object
pdf = PdfDocument()

# Load a PDF document
pdfPath = "C:/python_workspace/NEWITEMS/marketing_tools/flipbook/"
pdf.LoadFromFile(pdfPath+"JAN24_ENG.pdf")

# Iterate through all pages in the document
for i in range(pdf.Pages.Count):

    # Save each page as an PNG image
    fileName = pdfPath+"images/ToImage-{0:d}.png".format(i)
    with pdf.SaveAsImage(i) as imageS:
        imageS.Save(fileName)
pdf.Close()