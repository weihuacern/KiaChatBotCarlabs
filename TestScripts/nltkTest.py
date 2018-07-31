from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

if __name__ == "__main__":
  tokenizer = RegexpTokenizer(r'\w+')

  data = "Engine Start/Stop Button* To use the ENGINE START/STOP button, you  must have the Smart Key fob on your person or  inside the vehicle . To start the engine: 1 .  Depress the brake pedal 2 .   Press the ENGINE START/STOP button while  gear shift is in P (Park) (or while in Neutral for  Manual Gear Shift) To turn the engine OFF: 1 .  Move gear shift into Park 2 .  Press the ENGINE START/STOP button A B REMINDERS:    In an emergency situation while the vehicle is in motion, you are able to turn the  engine off and to the ACC position by pressing the ENGINE START/STOP button  for more than 2 seconds or 3 times successively within 3 seconds    If the Smart Key battery is weak or not working properly, hold the Smart Key fob  up to the ENGINE START/STOP button (Lock button side closest) and press to  start engine   QUICK TIPS   To use electrical accessories:  ACC position  A :   When in the OFF position and without depressing the brake pedal, press the ENGINE START/STOP button once ON position  B :   When already in the ACC position  A  and without depressing the brake pedal, press the ENGINE START/STOP button again   When in the OFF position and without depressing the brake pedal, press the ENGINE START/STOP button twice  B Keeping the vehicle in ACC or the ON position for extended periods of time without turning engine on may discharge the vehicles battery .   QR CODE   Engine Start/Stop Button  and Smart Key Video     To view a video on your  mobile device, snap this  QR Code or visit the listed  website . Refer to page 2 for more  information . www.KuTechVideos.com/ub13/2017 12"
  stopWords = set(stopwords.words('english'))
  #words = word_tokenize(data)
  words = tokenizer.tokenize(data)
  wordsFiltered = []
 
  #myStemmer = SnowballStemmer("english")
  myStemmer = PorterStemmer()
  myLemmatizer = WordNetLemmatizer()

  for w in words:
    if w not in stopWords:
      wordsFiltered.append( myStemmer.stem(w.lower()) )
      w_lemma_v = myLemmatizer.lemmatize(w.lower(), pos='v')
      w_lemma_vn = myLemmatizer.lemmatize(w_lemma_v, pos='n')
      w_lemma_vna = myLemmatizer.lemmatize(w_lemma_vn, pos='a')
      w_lemma_vnar = myLemmatizer.lemmatize(w_lemma_vna, pos='r')
      wordsFiltered.append( w_lemma_vnar )
 
  #print(myStemmer.stem("engine"))
  #print(myLemmatizer.lemmatize("engine"))
  print( myLemmatizer.lemmatize("apple", pos='v') )
  print( myLemmatizer.lemmatize( myLemmatizer.lemmatize("apples", pos='v'), pos='n' ) )
  print( myLemmatizer.lemmatize("am", pos='v') )
  print( myLemmatizer.lemmatize("is", pos='v') )
  print( myLemmatizer.lemmatize("are", pos='v') )
  print( myLemmatizer.lemmatize("were", pos='v') )
  print(wordsFiltered)
