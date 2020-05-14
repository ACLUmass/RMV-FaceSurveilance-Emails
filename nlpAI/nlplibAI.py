#https://medium.com/@bedigunjit/simple-guide-to-text-classification-nlp-using-svm-and-naive-bayes-with-python-421db3a72d34
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
import re
import nltk
from sklearn.datasets import load_files
#nltk.download('stopwords')
import pickle
from nltk.corpus import stopwords
from nltk.corpus import wordnet

def get_wordnet_pos(word):
  """Map POS tag to first character lemmatize() accepts"""
  tag = nltk.pos_tag([word])[0][1][0].upper()
  tag_dict = {"J": wordnet.ADJ,
              "N": wordnet.NOUN,
              "V": wordnet.VERB,
              "R": wordnet.ADV}

  return tag_dict.get(tag, wordnet.NOUN)



#clean up each review into a bag of common base forms called lemmas
#stemming does this crudely by chopping off endings. Lemmatization uses vocabulary and morphological analysis to do a better job.
def mkBow(X): #make bag of words from each document
  documents = []

  from nltk.stem import WordNetLemmatizer

  stemmer = WordNetLemmatizer()

  for sen in range(0, len(X)):
    # Remove all the special characters
    document = re.sub(r'\W', ' ', str(X[sen]))
    
    # remove all single characters
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
    
    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
    
    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)
    
    # Removing prefixed 'b'
    document = re.sub(r'^b\s+', '', document)
    
    # Converting to Lowercase
    document = document.lower()
    
    # Lemmatization

    document = document.split()

    tmp1 = []
    for word in document:
      tag = get_wordnet_pos(word)
      #tmp = stemmer.lemmatize(word, pos=tag) #doesn't improve results
      tmp = stemmer.lemmatize(word)
      if word != tmp:
        print(word,tmp)
      tmp1.append(tmp)
 
    #document = [stemmer.lemmatize(word) for word in document]
    document = ' '.join(document)

    documents.append(document)

  return documents


#from sklearn.feature_extraction.text import CountVectorizer
#create a class that maps lemmas from all the documents into numbers. It removes all the stopwords because they have no useful meaning.
#It ignores lemmas that appear in fewer than 5 documents, assuming they are anomylies that would distort classification and it ignores lemmas
#that occur in over 70% of the documents because those are not useful for discrimination. Finally, limit us 1500 unique lemmas because low
#low frequency ones aren't useful. 
#vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))

#for each document count the frequency of each lemma and return it as a 2D matrix 
#X = vectorizer.fit_transform(documents).toarray()

#normalize this raw count to a weighted one 
#from sklearn.feature_extraction.text import TfidfTransformer
#tfidfconverter = TfidfTransformer()
#X = tfidfconverter.fit_transform(X).toarray()

def mkSet(documents):
#alternate to above block
#create a class that maps lemmas from all the documents into numbers. It removes all the stopwords because they have no useful meaning.
#It ignores lemmas that appear in fewer than 5 documents, assuming they are anomylies that would distort classification and it ignores lemmas
#that occur in over 70% of the documents because those are not useful for discrimination. Finally, limit us 1500 unique lemmas because low
#low frequency ones aren't useful. 
  from sklearn.feature_extraction.text import TfidfVectorizer
  tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
  #tfidfconverter = TfidfVectorizer(sublinear_tf=True,max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
#for each document count the frequency of each lemma and return it as a 2D matrix. This is a normalized frequency from 0 to 1 weighted by the
#inverse number of documents each term occurs in. The purpose is to lower the impact of terms that occur in lots of documents  

#for each document count the frequency of each lemma and return it as a 2D matrix 
  X = tfidfconverter.fit_transform(documents).toarray()
#print(len(X))
#print(X[0:10][0:10])

#using y which tells us True/False for each document, split X into an 80% training set and a 20% test set. 
  #from sklearn.model_selection import train_test_split
  #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0) #set random seed so results don't vary over runs
  #return(X_train,X_test,y_train,y_test)
  return(X)


#===================================================
def rfa(X_train,X_test,y_train):
  from sklearn.ensemble import RandomForestClassifier
#https://stackabuse.com/random-forest-algorithm-with-python-and-scikit-learn/
  classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
  #classifier = RandomForestClassifier(n_estimators=2000, random_state=0)
  classifier.fit(X_train, y_train) #train the classifier 
  y_pred = classifier.predict(X_test) #generate the True/False matrix for the test set
  return(y_pred)

#++++++++++++===++++++++++++++++++++++++++++++++++++
def svm(X_train,X_test,y_train):
  from sklearn import svm
  SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
  SVM.fit(X_train,y_train)
  y_pred = SVM.predict(X_test)
  return(y_pred)

#++++++++++++===++++++++++++++++++++++++++++++++++++
def nvb(X_train,X_test,y_train):
  from sklearn import naive_bayes
  Naive = naive_bayes.MultinomialNB()
  Naive.fit(X_train,y_train)
  y_pred = Naive.predict(X_test)
  return(y_pred)
#exit()


#movie_data = load_files(r"review_polarity/txt_sentoken")
#X is an array of strings where each srting is a review of the form b"........"
#y is an array of zeros and ones of the same length 1=positive 0=negative
#X, y = movie_data.data, movie_data.target

#documents = mkBow(X) #make "bag of words" out of every document
#X_train - list of documents in form b"......." for training AI
#y_train - list of 0/1 false/true for X_train
#X_test - list of documents in form b"......." for testing AI
#y_test - list of 0/1 false/true for X_test
#X_train,X_test,y_train,y_test = mkSet(documents)
#y_pred = nvBayes(X_train,X_test,y_train)
#y_pred = svm(X_train,X_test,y_train)
#y_pred = rfc(X_train,X_test,y_train)

#from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
#print(confusion_matrix(y_test,y_pred)) 
#[[true negatives,  false positives]
# [false negatives, true positives]]
#true negative: y_test=false, y_pred=false - big number means selectivity is good
#true positive: y_test=true, y_pred=true - big number means sensitivity is good
#false negative: y_test=true, y_pred=false - classifier misses a true document - big number means sensitivity is low
#false positive: y_test=false, y_pred=true - classifier incorrectly calls a false document as ture - big number means selectivity is poor

#print(accuracy_score(y_test, y_pred)) # the percentage of correct predictions

#print(classification_report(y_test,y_pred))
#precision = what fraction of positives are correct
#recall = what fraction of all positives have been found
#support = actual number of positives in test set
#f1 = 2/(1/prec. + 1/recall) f1 = 1.0 if precision and recall are perfect

#exit()

#with open('text_classifier', 'wb') as picklefile:
#    pickle.dump(classifier,picklefile)

#####################################################
#with open('text_classifier', 'rb') as training_model:
#    model = pickle.load(training_model)

#y_pred2 = model.predict(X_test)

#print(confusion_matrix(y_test, y_pred2))
#print(classification_report(y_test, y_pred2))
#print(accuracy_score(y_test, y_pred2)) 

