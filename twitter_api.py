import tweepy
import configparser
import pandas as pd

import re
import string

import wordsegment

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go


import numpy as np
import wordsegment as ws
import preprocessor as pre
import contractions

import pickle
import warnings
warnings.filterwarnings("ignore")


stop_words = set(stopwords.words("english"))
# Load segmentation dictionary
ws.load()
# Set options for Twitter processing - remove url, mention, and emojis
pre.set_options(pre.OPT.URL, pre.OPT.EMOJI, pre.OPT.MENTION, pre.OPT.SMILEY, pre.OPT.HASHTAG)

from wordcloud import WordCloud
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


def api_access():
    
    # read configs
    config = configparser.ConfigParser()
    config.read('config.ini')

    api_key = config['twitter']['api_key']
    api_key_secret = config['twitter']['api_key_secret']

    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']
    
    # Authentication Handler
    auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
    auth.set_access_token(access_token,access_token_secret)
    return auth




# extract the hastags
def hashtags_extract(tweets):
    hashtags = []
    #loop words in the tweet
    for tweet in tweets:
        ht = re.findall(r"#(\w+)", tweet)
        hashtags.append(ht)
    return hashtags

#df['hashtags'] = hashtags_extract(df['Tweet'])

# Preprocess Tweet
def pre_tweet_API(tweet):
    
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

#df['clean_tweet'] = df['Tweet'].apply(lambda tweet: pre_twitter(tweet))

# print(df["clean_tweet"].duplicated().value_counts())
#print("\n .................. \n")

#df["clean_tweet"] =df["clean_tweet"].drop_duplicates()

#print(df["clean_tweet"].duplicated().value_counts())
#print("\n .................. \n Null values")

#print(df["clean_tweet"].isnull().sum())
#print("\n .................. \n Droping Null values")

#df = df.dropna()
#print("\n .................. \n After droping Null values")

#print(df["clean_tweet"].duplicated().value_counts())


# Logistic Regression
with open("D:\\Study\\FYP\\app\\FYPv1_1_LR_pipeline_model.pkl",'rb') as f:
    modelObj1 = pickle.load(f)




def twitter_live_exp(object,text,name='Model'):
    
    result =object.predict([text])[0]
    resultValue = ''

   # print(result)
    if result == 1:
        resultValue = 1
    else:
        resultValue = 0
    return resultValue


def twitter_live_exp_sent(object,text,name='Model'):
    
    result =object.predict([text])[0]
    resultValue = ''
    # print(result)
    if result == 1:
        resultValue = 'Relevant_Tweet'
    else:
        resultValue = 'Irrelevant_Tweet'
    return resultValue
    


# This utility function will be used to evaluate the other models also.
labels = ['negative','positive']
def show_performance_data(Y_test, Y_pred, model_name):
  print(classification_report(Y_test, Y_pred, target_names=labels))
  tmp_result = classification_report(Y_test, Y_pred, target_names=labels, output_dict=True)
  cm1 = confusion_matrix(Y_test, Y_pred)
  df_cm = pd.DataFrame(cm1, index = [i for i in labels], columns = [i for i in labels])
  plt.figure(figsize = (7,5))
  sns.heatmap(df_cm, annot=True,cmap='gist_earth_r', fmt='g')
  plt.savefig('confusion_mrtx_'+model_name+'.png',bbox_inches = 'tight')
  return tmp_result

