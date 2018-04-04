import os
import PyPDF2

class PDFDecryptor:
  def __init__(self, inputfname_list):
    self.inputfname_list = inputfname_list
    return

  def DecrypteOnePDF(self, fname):
    di = "../RawPDF/"
    do = "../DecryptedPDF/"
    fp = di + fname
    src_pdf = PyPDF2.PdfFileReader(open(fp, "rb"))

    if src_pdf.isEncrypted:
      try:
        pdfFile.decrypt('')
        print ('File Decrypted (PyPDF2)')
      except:
        fn_new = do + "qpdfHacked_" + fname
        cmd = "cp "+ fp +" temp.pdf; qpdf --password='' --decrypt temp.pdf " + fn_new + "; rm temp.pdf"
        print(cmd)
        os.system(cmd)
        print('File Decrypted (qpdf)')
    else:
      print ('File Not Encrypted')
    
    return

  def DecrypteAllPDF(self):
    for fname in self.inputfname_list:
      self.DecrypteOnePDF( fname )
    return

class PDFToSQLText:
  def __init__(self, fname):
    self.fname = fname
    return
 
  def GetTextOnePage(self, ):
    # creating a pdf file object
    pdfFileObj = open('2019-Ford-Lincoln-Supplement-version-1_su_EN-US_03_2018.pdf', 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # printing number of pages in pdf file
    print(pdfReader.numPages)

# creating a page object
pageObj = pdfReader.getPage(5)

# extracting text from page
print(pageObj.extractText().encode('utf-8'))
print(type(pageObj.extractText()))
# closing the pdf file object
pdfFileObj.close()

  .getNumPages() 
  # designed (index) schema: filename, year, make, doc type, page number, text

class PDFToSQLImage:
  def __init__(self, fname):
    return

  # designed (index) schema: filename, page number, image byte

if __name__ == "__main__":

  #rawfname_list = ['2017_Rio_FFG.pdf', '2017_Rio_NaviQG.pdf', '2017_Rio_NaviUM.pdf', '2017_Rio_OM.pdf', '2017_Rio_UVOQG.pdf', '2017_Rio_UVOUM.pdf']
  #myPDFDecryptor = PDFDecryptor(rawfname_list)
  #myPDFDecryptor.DecrypteAllPDF()


