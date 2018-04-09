import struct
import PyPDF2
#from PIL import Image
from wand.image import Image
import io

def tiff_header_for_CCITT(width, height, img_size, CCITT_group=4):
  tiff_header_struct = '<' + '2s' + 'h' + 'l' + 'h' + 'hhll' * 8 + 'h'
  return struct.pack(tiff_header_struct,
                     b'II',  # Byte order indication: Little indian
                     42,  # Version number (always 42)
                     8,  # Offset to first IFD
                     8,  # Number of tags in IFD
                     256, 4, 1, width,  # ImageWidth, LONG, 1, width
                     257, 4, 1, height,  # ImageLength, LONG, 1, lenght
                     258, 3, 1, 1,  # BitsPerSample, SHORT, 1, 1
                     259, 3, 1, CCITT_group,  # Compression, SHORT, 1, 4 = CCITT Group 4 fax encoding
                     262, 3, 1, 0,  # Threshholding, SHORT, 1, 0 = WhiteIsZero
                     273, 4, 1, struct.calcsize(tiff_header_struct),  # StripOffsets, LONG, 1, len of header
                     278, 4, 1, height,  # RowsPerStrip, LONG, 1, lenght
                     279, 4, 1, img_size,  # StripByteCounts, LONG, 1, size of image
                     0  # last IFD
                    )

#https://gist.github.com/jrsmith3/9947838
#https://github.com/ronanpaixao/PyPDFTK/blob/master/pdf_images.py

def pdf_page_to_png(src_pdf, pagenum = 0, resolution = 72):
    """
    Returns specified PDF page as wand.image.Image png.
    :param PyPDF2.PdfFileReader src_pdf: PDF from which to take pages.
    :param int pagenum: Page number to take.
    :param int resolution: Resolution for resulting png in DPI.
    """
    dst_pdf = PyPDF2.PdfFileWriter()
    dst_pdf.addPage(src_pdf.getPage(pagenum))

    pdf_bytes = io.BytesIO()
    dst_pdf.write(pdf_bytes)
    pdf_bytes.seek(0)

    print(pdf_bytes)
    #img = Image.open(pdf_bytes)
    img = Image(file = pdf_bytes)
    #img = Image(file = pdf_bytes, resolution = resolution)
    img.convert("png")

    return img

if __name__ == '__main__':
    src_pdf = PyPDF2.PdfFileReader(open("../DecryptedPDF/qpdfHacked_2018_Rio_OM.pdf", "rb"))
    #src_pdf = PyPDF2.PdfFileReader(open("../RawPDF/2018_Rio_OM.pdf", "rb"))
    #src_pdf = PyPDF2.PdfFileReader(open("/Users/ustc-weihua/Desktop/CarlabsKIA/2017_Rio_NaviQG.pdf", "rb"))
    #src_pdf = PyPDF2.PdfFileReader(open("/Users/ustc-weihua/Desktop/CarlabsKIA/2007_Rio_FFG.pdf", "rb"))
    print (src_pdf.getIsEncrypted())
    #src_pdf.decrypt('')
    print (src_pdf.getNumPages())
  
    #page = src_pdf.getPage(0)
    img = pdf_page_to_png(src_pdf, pagenum = 0)
    img.save(filename = "testpage0_2018_Rio_OM.png")
    img = pdf_page_to_png(src_pdf, pagenum = 3)
    img.save(filename = "testpage9_2018_Rio_OM.png")
    #img.transform("", "200")
    #img.save(filename = small_filename)

