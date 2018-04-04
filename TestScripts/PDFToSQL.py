import os
import PyPDF2


def DecryptePDF( fname ):
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
      command = "cp "+ fp +" temp.pdf; qpdf --password='' --decrypt temp.pdf " + fn_new + "; rm temp.pdf"
      os.system(command)
      print('File Decrypted (qpdf)')
  else:
    print ('File Not Encrypted')


if __name__ == "__main__":
  DecryptePDF( '2017_Rio_OM.pdf' )
