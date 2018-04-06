import os
import re
import PyPDF2
import pandas as pd
import sqlalchemy
import io

#ok PyPDF2 sucks! move to pdfminer for text
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator

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

    # Open and read the pdf file in binary mode
    fp = open(self.d + self.fname, 'rb') 
    # Create parser object to parse the pdf content
    parser = PDFParser(fp)

    # Store the parsed content in PDFDocument object
    document = PDFDocument(parser, "")

    # Check if document is extractable, if not abort
    if not document.is_extractable:
      raise PDFTextExtractionNotAllowed

    # Create PDFResourceManager object that stores shared resources
    # such as fonts or images
    rsrcmgr = PDFResourceManager()

    # set parameters for analysis
    laparams = LAParams()

    # Create a PDFDevice object which translates interpreted
    # information into desired format
    # Device to connect to resource manager to store shared resources
    # device = PDFDevice(rsrcmgr)
    # Extract the decive to page aggregator to get LT object elements
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create interpreter object to process content from PDFDocument
    # Interpreter needs to be connected to resource manager for shared
    # resources and device
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Ok now that we have everything to process a pdf document,
    # lets process it page by page
    numpages = 0
    # index for dataframe
    index = 0
    for page in PDFPage.create_pages(document):
      # Initialize the text for every page
      extracted_text = ""
      # As the interpreter processes the page stored in PDFDocument object
      interpreter.process_page(page)
      # The device renders the layout from interpreter
      layout = device.get_result()
      # Out of the many LT objects within layout, we are interested
      # in LTTextBox and LTTextLine
      for lt_obj in layout:
        if (isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine)):
          extracted_text += lt_obj.get_text()
      
      numpages += 1
      thistexts = (extracted_text.encode('utf-8').strip()).split(b'.')
      asctexts = (extracted_text.encode('utf-8').strip()).decode("ascii", "ignore").replace("\n"," ").strip()
      df.loc[index] = [self.fname, year, model, doctype, numpages, asctexts]
      index += 1
      '''
      for thistext in thistexts:
        asctext = thistext.decode("ascii", "ignore").replace("\n"," ").strip()
        if numpages < 4:
          print (asctext)
        if ( len(asctext) > 0 ):
          #asctext = thistext.decode("ascii", "ignore")
          #if numpages < 4:
          #  print(asctext)
          df.loc[index] = [self.fname, year, model, doctype, numpages, asctext]
          index += 1
      '''
    return df
    # Bye, PyPDF2, you sucks!
    '''
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
    '''

class PDFToSQLImage:
  def __init__(self, d, fname):
    self.d = d
    self.fname = fname
    return

  def ConvertToPandas(self):
    # designed (index) schema: filename, page number, image byte
    df = pd.DataFrame( columns=['filename', 'pagenum', 'image'] )

    # Open and read the pdf file in binary mode
    pdfReader = PyPDF2.PdfFileReader(open(self.d + self.fname, 'rb'))
    totpagnums = pdfReader.numPages
    index = 0
    for i in range(totpagnums):
      pdfWriter = PyPDF2.PdfFileWriter()
      pdfWriter.addPage(pdfReader.getPage(i))
      pdf_bytes = io.BytesIO()
      pdfWriter.write(pdf_bytes)
      pdf_bytes.seek(0)
      #print(pdf_bytes)
      df.loc[index] = [self.fname, i+1, pdf_bytes]
      index += 1

    return df

if __name__ == "__main__":

  #rawfname_list = ['2017_Rio_FFG.pdf', '2017_Rio_NaviQG.pdf', '2017_Rio_NaviUM.pdf', '2017_Rio_OM.pdf', '2017_Rio_UVOQG.pdf', '2017_Rio_UVOUM.pdf']
  #rawfname_list = ['2018_Rio_OM.pdf']
  #myPDFDecryptor = PDFDecryptor(rawfname_list)
  #myPDFDecryptor.DecrypteAllPDF()
  
  #myPDFToSQLText = PDFToSQLText( "../RawPDF/", "2017_Rio_FFG.pdf" )
  #myPDFToSQLText = PDFToSQLText( "../DecryptedPDF/", "qpdfHacked_2018_Rio_OM.pdf" )
  #print(myPDFToSQLText.GetTextOnePage(31))
  #df_text = myPDFToSQLText.ConvertToPandas()
  #print (df_text.head())
  #print (df_text.describe())
  #print (len(df_text))
  #engine = sqlalchemy.create_engine('sqlite:///KIATextInfo.db')
  #df_text.to_sql(name = 'Test', con = engine, if_exists = 'replace', index = False)


  myPDFToSQLImage = PDFToSQLImage( "../DecryptedPDF/", "qpdfHacked_2018_Rio_OM.pdf" )
  df_image = myPDFToSQLImage.ConvertToPandas()
  engine = sqlalchemy.create_engine('sqlite:///KIAImageInfo.db')
  df_image.to_sql(name = 'Test', con = engine, if_exists = 'replace', index = False)
