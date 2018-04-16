from sklearn.pipeline import Pipeline
from sklearn import base

import pandas as pd
import numpy as np

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import sqlite3

import gensim

#input is a pandas data frome, out put is a list
class ColumnSelectorTokenization(base.BaseEstimator, base.TransformerMixin):
  def __init__(self, copy_colnames, token_colnames):
    self.copy_colnames = copy_colnames  # We will need these in transform()
    self.token_colnames = token_colnames
    
  def fit(self, X, y=None):
    # This transformer doesn't need to learn anything about the data,
    # so it can just return self without any further processing
    return self
    
  def transform(self, X):
    alldata = pd.DataFrame(columns = self.copy_colnames + self.token_colnames)
    idx = 0
    for index, row in X.iterrows():
      onedata = []
      for colname in self.copy_colnames:
        onedata.append(row[colname])
      for colname in self.token_colnames:
        for x in self.tokenization(row[colname]):
          onedata.append(x)
      if len(onedata) > len(self.copy_colnames):
        alldata.loc[idx] = onedata
        idx += 1
        #alldata.append(onedata)
    return alldata

  def tokenization(self, text):
    sentences = []
    tokenizer = RegexpTokenizer(r'\w+')
    stopWords = set(stopwords.words('english'))
    
    wordsFiltered = []
    words = tokenizer.tokenize(text)
    for w in words:
      wlower = w.lower()
      if wlower not in stopWords:
        if len(wlower) > 1: # filter short word
          wordsFiltered.append(wlower)
    if len(wordsFiltered) > 0:
      sentences.append(wordsFiltered)
    return sentences

if __name__ == "__main__":

  # Create your connection.
  con = sqlite3.connect('KIATextInfo.db')
  cursor = con.cursor()
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
  sqlcmds = [ ("SELECT * FROM `" + x[0] + "`;") for x in (cursor.fetchall()) ]
  df = pd.DataFrame()
  for sqlcmd in sqlcmds:
    tmpdf = pd.read_sql_query(sqlcmd, con)
    df = df.append(tmpdf)
  
  print(len(df))
  #filename pagenum text
  pre = ColumnSelectorTokenization(['filename', 'pagenum'], ['text'])
  res = pre.fit_transform(df)
  #print(res['text'].values)

  model = gensim.models.Word2Vec(res['text'].values, min_count=1)
  #print(model.similarity('feature', 'fuel'))
  score_res = []
  for target in res['text'].values:
    score_res.append( ( target, model.n_similarity(['speed', 'limit', 'alert'], target) ) )
    #print(model.n_similarity(['speed', 'limit', 'alert'], target))

  sorted_score_res = sorted(score_res, key=lambda x: x[1])
  print( sorted_score_res[0] )
  print( sorted_score_res[1] )
  print( sorted_score_res[-1] )
  print( sorted_score_res[-2] )
  #word2vec_pipeline = Pipeline([
  #        ('FitTransform', ColumnSelectorTokenization(['filename', 'pagenum'], ['text'])
  #        ('SimilarityCalc', )
  #    ])
  #Note, alpha 10 is better than alpha 0.5
  #res = word2vec_pipeline.fit_transform(df)
  #for entry in res:
  #  print(entry[-1])
