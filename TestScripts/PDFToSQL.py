import os
import re
import PyPDF2
import pandas as pd
import sqlalchemy

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
  def __init__(self, d, fname):
    self.d = d
    self.fname = fname
    return
 
  def GetTextOnePage(self, pagenum):
    # creating a pdf file object
    pdfFileObj = open(self.d + self.fname, 'rb')
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # total number of pages in pdf file
    totpagnums = pdfReader.numPages
    # creating a page object
    pageObj = pdfReader.getPage(pagenum)
    # extracting text from page
    thistext = pageObj.extractText().encode('utf-8')
    #thistext = (pageObj.extractText().encode('utf-8')).decode("utf-8")
    #print(type(pageObj.extractText()))
    
    #for i in range(totpagnums):
    #  pageObj = pdfReader.getPage(i)
      # extracting text from page
    #  print(pageObj.extractText().encode('utf-8'))
    #  print(type(pageObj.extractText()))

    # closing the pdf file object
    pdfFileObj.close()
    return thistext

  def ConvertToPandas(self):
  # designed (index) schema: filename, year, model, doc type, page number, text
    df = pd.DataFrame( columns=['filename', 'year', 'model', 'doctype', 'pagenum', 'text'] )
    docinfo = self.fname.split('_')
    #print (docinfo)
    if( len(docinfo) == 3 ):
      year, model, doctype = self.fname.split('_')
    elif( len(docinfo) == 4 ):
      tmp, year, model, doctype = self.fname.split('_')
    else:
      print(self.fname)
      print("Wrong file name, please check!")
      return

    pdfFileObj = open(self.d + self.fname, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    totpagnums = pdfReader.numPages
    print(totpagnums)
    index = 0
    for i in range(totpagnums):
      pageObj = pdfReader.getPage(i)
      # extracting text from page
      thistexts = (pageObj.extractText().encode('utf-8').strip()).split(b'.')
      #print(thistexts.split(b'\n'))
      #print(len(thistexts.split(b'\n')))
      for thistext in thistexts:
        #print (thistext)
        if ( len(thistext) > 0 and re.compile(b"^[A-Za-z]").match(thistext) ):
          asctext = thistext.decode("ascii", "ignore")
          if i <= 4:
            print (i)
            print (pageObj)
            #print (asctext)
            #print (thistext)
          #print(re.compile(b"^[A-Za-z]").match(thistext))
          df.loc[index] = [self.fname, year, model, doctype, i, asctext]
          index += 1

    return df
    

class PDFToSQLImage:
  def __init__(self, fname):
    return

  # designed (index) schema: filename, page number, image byte

if __name__ == "__main__":

  #rawfname_list = ['2017_Rio_FFG.pdf', '2017_Rio_NaviQG.pdf', '2017_Rio_NaviUM.pdf', '2017_Rio_OM.pdf', '2017_Rio_UVOQG.pdf', '2017_Rio_UVOUM.pdf']
  #myPDFDecryptor = PDFDecryptor(rawfname_list)
  #myPDFDecryptor.DecrypteAllPDF()
  
  #myPDFToSQLText = PDFToSQLText( "../RawPDF/", "2017_Rio_FFG.pdf" )
  myPDFToSQLText = PDFToSQLText( "../DecryptedPDF/", "qpdfHacked_2017_Rio_OM.pdf" )
  #print(myPDFToSQLText.GetTextOnePage(31))
  df = myPDFToSQLText.ConvertToPandas()
  print (df.head())
  print (df.describe())
  print (len(df))

  engine = sqlalchemy.create_engine('sqlite:///KIATextInfo.db')
  df.to_sql(name = 'Test', con = engine, if_exists = 'replace', index = False)
