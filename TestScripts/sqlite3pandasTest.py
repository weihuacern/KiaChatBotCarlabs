import sqlite3
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

if __name__ == '__main__':
  # Create your connection.
  con = sqlite3.connect('KIATextInfo.db')
  cursor = con.cursor()
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
  #tablenames = [ x[0] for x in (cursor.fetchall()) ]
  #print(tablenames)
  sqlcmds = [ ("SELECT * FROM `" + x[0] + "`;") for x in (cursor.fetchall()) ]
  print(sqlcmds)
  df = pd.read_sql_query(sqlcmds[0], con)
  #df = pd.read_sql('SELECT * FROM `2017_Rio_FFG`;', con)
  #print(df.head(5))

  sentences = []
  tokenizer = RegexpTokenizer(r'\w+')
  stopWords = set(stopwords.words('english'))
  for i in range(5):
    wordsFiltered = []
    words = tokenizer.tokenize(df.loc[i]['text'])
    for w in words:
      if w not in stopWords:
        wordsFiltered.append(w.lower())
    if len(wordsFiltered) > 0:
      sentences.append(wordsFiltered)

  print(sentences)


