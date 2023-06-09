# -*- coding: utf-8 -*-
"""Recommender_ContentBasedFiltering

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gx3C0ogfs3zc3v21suZavdWQKYY4b-qa
"""

#!/usr/bin/env/ python3

pip install nltk

pip install surprise

from surprise import Dataset
from surprise import KNNBasic
import pandas as pd
import nltk
import re
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from google.colab import files
from surprise.model_selection import train_test_split

uploaded = files.upload()

# Load the dataset (example: MovieLens 100K)
data = pd.read_csv("umkm.csv")
produk = pd.read_excel('umkm_products.xlsx')
produk.head()

data.shape

deskripsi = data['Deskripsi_usaha']
deskripsi.head()

"""#Tokenizer"""

nltk.download("punkt")

tokenized_sent = nltk.sent_tokenize(str(deskripsi))
tokenized_sent

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()

X = vectorizer.fit(tokenized_sent)

print(X.vocabulary_)

vectorizer = CountVectorizer(lowercase=False)

X = vectorizer.fit(tokenized_sent)
print(X.vocabulary_)

nltk.download('stopwords')

#list_stopwords = set(stopwords.words('indonesian'))

#sw = vectorizer.get_stop_words()
#print(sw)

vectorizer = CountVectorizer(stop_words=stopwords.words('indonesian'))
x = vectorizer.fit(tokenized_sent)
print(x.vocabulary_)

"""#TF-IDF"""

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words=stopwords.words('indonesian'))

tf_results = tfidf.fit_transform(tokenized_sent)

print(tf_results)

print(tfidf.get_feature_names_out())

tfidf_token = tfidf.get_feature_names_out()

df_CountVector = pd.DataFrame(data = tf_results.toarray(), columns = tfidf_token)
print(df_CountVector)

word_count = pd.DataFrame({
    'word': tfidf_token,
    'tf-idf score': tf_results.sum(axis = 0).flat
})

word_count

word_count.sort_values(by = ['tf-idf score'], ascending = False) #Showing by descending order

"""#Training and Testing"""

from sklearn.model_selection import train_test_split

# Define the collaborative filtering algorithm
algo = KNNBasic()

# Train the algorithm on the training set
algo.fit(trainset)

# Make predictions on the test set
predictions = algo.test(testset)

# Print the predicted ratings for each user-item pair in the test set
for prediction in predictions:
    print(f"User {prediction.uid} -> Item {prediction.iid} : Predicted Rating {prediction.est}")

"""#Function to Content_Based Recommendation System"""

from sklearn.metrics.pairwise import cosine_similarity

# Matching the category with the dataset and reset the index
category = data['category']

def recommend(nama_usaha, category):
  datacat = data.loc[data['category'] == category]  
  datacat.reset_index(level = 0, inplace = True) 
  nama_usaha = datacat['nama_usaha']
    # Convert the index into series
  indices = pd.Series(datacat.index, index = datacat['nama_usaha'])
    
    #Converting the place name into vectors and used bigram
  tf = TfidfVectorizer(analyzer='word', ngram_range=(2, 2), min_df = 1, stop_words='english')
  tfidf_matrix = tf.fit_transform(datacat['nama_usaha'])
    
    # Calculating the similarity measures based on Cosine Similarity
  sg = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # Get the index corresponding to produk

  idx = indices[nama_usaha]
  sig = list(enumerate(sg[idx]))
  sig = sorted(sig, key=lambda x: x[1][0], reverse=True)
  sig = sig[1:6]
  produk_indices = [i[0] for i in sig]
   
    # Top 5 recommendation
  rec = data[['nama_usaha', 'category']].iloc[produk_indices]
  print(rec)     
  
  #rec  
  #for i in rec['','Category']:
      #print(i)
      #img = Image.open(BytesIO(response.content))
      #plt.figure()
      #print(plt.imshow(img))