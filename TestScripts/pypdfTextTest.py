# importing required modules
import PyPDF2
 
if __name__ == '__main__':
  # creating a pdf file object
  pdfFileObj = open('../RawPDF/2017_Rio_UVOUM.pdf', 'rb')
 
  # creating a pdf reader object
  pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
 
  # printing number of pages in pdf file
  print(pdfReader.numPages)
 
  # creating a page object
  pageObj = pdfReader.getPage(117)
 
  # extracting text from page
  print(pageObj.extractText().encode('utf-8'))
  print(type(pageObj.extractText()))
  # closing the pdf file object
  pdfFileObj.close()
