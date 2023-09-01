import re
import string

import wordsegment

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go


import numpy as np
import wordsegment as ws
import preprocessor as pre
import contractions
import warnings
warnings.filterwarnings("ignore")
import pickle


stop_words = set(stopwords.words("english"))
# Load segmentation dictionary
ws.load()
# Set options for Twitter processing - remove url, mention, and emojis
pre.set_options(pre.OPT.URL, pre.OPT.EMOJI, pre.OPT.MENTION, pre.OPT.SMILEY, pre.OPT.HASHTAG)




def pre_tweet(tweet):
    
    # Remove mails
    tweet = ' '.join([item for item in tweet.split() if '@' not in item])
    
    # Clean emoji, Url, mentions, Hashtags
    tweet = pre.clean(tweet)
    
    # Word Segentation
    tweet = " ".join(wordsegment.segment(tweet))
 
    # Converting to Lowercase
    tweet = tweet.lower()
    
     # Contraction fix (haven't, isn't etc)
    tweet = contractions.fix(tweet)
    
    # Punctuations removal
    tweet = tweet.translate(str.maketrans(" ", " ", string.punctuation))
    
    # Remove digits and Special characters
    tweet = re.sub('[^a-zA-Z#]',' ',tweet)
    
    # Remove extra spaces
    tweet = re.sub('\s+',' ',tweet)
    
    #Tokenizer
    token=nltk.tokenize.RegexpTokenizer(r'\w+')
    #applying token
    tweet_token = token.tokenize(tweet)

    #removing stop words
    filter_words = [w for w in tweet_token if w not in stopwords.words('english')]

    #stemmering the text and joining
    stemmer = nltk.stem.PorterStemmer()
    tweet = [stemmer.stem(w) for w in filter_words]

    
    return " ".join(tweet)





# Logistic Regression
with open("D:\\Study\\FYP\\app\\FYPv1_1_LR_pipeline_model.pkl",'rb') as f:
    modelObj = pickle.load(f)




def prep(text):
    return pre_tweet(text)

def liveExample(object,text,name='Model'):
    
    #print("Model Name : "+name)
    
    test = pre_tweet(text)
    #print(test)
    
    result =object.predict([test])[0]
    #print("Relevance =",result)
    resultValue = ''

    # print(result)
    #for i in result:
    if result == 1:
        resultValue = 'Relevant_Tweet'
    else:
        resultValue = 'Irrelevant_Tweet'
    return resultValue
    

