
import streamlit as st
from streamlit_option_menu import option_menu
import json
from streamlit_lottie import st_lottie

from sympy import expand
from UserInput import *
from PIL import Image
from twitter_api import *
from realTimeFetch import *
from alert import *
# Twitter API
import tweepy
import configparser
import pandas as pd

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import plotly.graph_objects as go


import pandas as pd
import re
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from PIL import Image

import warnings
warnings.filterwarnings("ignore")



def Subheader(url):
    st.markdown(f'<p style="color:#00acee ;font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def load_lottiefile(filepath: str):
     with open (filepath,'r') as f:
          return json.load(f)

def bold_text(url):
     st.markdown(f"<h3 style='text-align: center;border-radius:2%;color: red;'>{url}</h3>", unsafe_allow_html=True)
     
def do_process_eng_hashtag(input_text: str) -> str:
    return re.sub(
        r'#[a-z]\S*',
        lambda m: ' '.join(re.findall('[A-Z][^A-Z]*|[a-z][^A-Z]*', m.group().lstrip('#'))),
        input_text,
    )

def header(url):
	st.markdown(f"<h1 style='text-align: center;border-radius:2%;color: #00acee ;'>{url}</h1>", unsafe_allow_html=True)


# extract the hastags
def hashtags_extract(tweets):
    hashtags = []
    #loop words in the tweet
    for tweet in tweets:
        ht = re.findall(r"#(\w+)", tweet)
        hashtags.append(ht)
    return hashtags



im = Image.open("D:\\Study\\FYP\\app\\Pictures\\2993737_twitter_social media_icon.png")
st.set_page_config(page_title="Disaster Monitor", page_icon=im)

import warnings
warnings.filterwarnings("ignore")
def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)



lottie_hello = load_lottiefile('D:\\Study\\FYP\\app\\animations\\70339-twitter-logo-animation.json')

#imag = st_lottie(lottie_hello,key="Hello")

with st.sidebar:
    st_lottie(lottie_hello,key="Hello", loop=True,speed=0.5, reverse=False)




st.set_option('deprecation.showPyplotGlobalUse', False)




choose = option_menu(None, ["Home" ,"AnalyzeTweets", "Dataset"],
                        icons=['house', 'kanban', 'pie-chart-fill'],
                        #menu_icon="app-indicator", 
                        default_index=0,
                        orientation="horizontal",
                        
                        styles={"color:#1e2b40"
    "container": {"padding": "5!important", "background-color": "#fafafa"},
    "icon": {"color": "orange", "font-size": "25px"},
    "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#676a6e"},
    "nav-link-selected": {"background-color": "#FF4B4B"},
}
)
    
    
    #logo = Image.open(r'C:\Users\13525\Desktop\Insights_Bees_logo.png')
#profile = Image.open(r'C:\Users\13525\Desktop\medium_profile.png')
if choose == "Home":

    def load_lottiefile(filepath: str):
        with open (filepath,'r') as f:
            return json.load(f)

    st.markdown("<h1 style='text-align: center; color: #00acee ;'>WELCOME TO</h1>"
        "<h2 style='text-align: center; color: #00acee ;'>Using Twitter and Machine Learning For Disaster Monitoring</h2>", unsafe_allow_html=True)
    st.write("\n")
    st.write("\n")
    st.write("\n")

    lottie_hello = load_lottiefile('D:\\Study\\FYP\\app\\animations\\computer1.json')

    col1,col2 = st.columns(2)
    col1.markdown("<div style='text-align: justify;text-justify: auto;filter:alpha(opacity=50); opacity:0.7;' class = 'center'>We are here to let you freely access our website. We aim to provide you with the ability to get Twitter data and test it using our trained model. This will help you check if the tweets are related to a specific type of disaster. Furthermore, you can view our dataset and the accuracy of trained models. We have tested different models based on the best accuracy we have selected that model for the prediction and analyzing of twitter data. Alert will be sent automatically to the concerned authorities of disaster management if the accuracy of the imported tweets from Twitter API matches the given parameters that we have defined. You can freely type any tweet and see the predicted results of the tweet. We hope you find our website useful.</div>", unsafe_allow_html=True)
    with col2:
        st_lottie(lottie_hello, loop=True,speed=1, reverse=False,width=300, height=350)


elif choose == "AnalyzeTweets":

	selected = st.sidebar.selectbox("Select Input Method", ("-", "User Input", "Import From Twitter API"))

	# For blank Page
	if selected == "-":
		st.markdown("<h1 style='text-align: center; color: #00acee ;'>Disaster Monitoring Using Twitter</h1>"
		#"<h2 style='text-align: center; color:#00acee ;'>Use Either @User or Twitter API Import</h2>"
		,unsafe_allow_html=True)
		st.write("\n")
		st.write("\n")
		st.write("\n")
		
		lottie_hello = load_lottiefile('D:\\Study\\FYP\\app\\animations\\graphs.json')

		col1,col2 = st.columns(2)
		with col1:
			st_lottie(lottie_hello, loop=True,speed=1, reverse=False,width=300, height=350)
		col2.markdown("<div style='text-align: justify;text-justify: auto;filter:alpha(opacity=50); opacity:0.7;' class = 'center'>Disaster Monitoring is the process of tweets extraction from twitter API for preprocessing purpose, after preprocessing the feature extraction from tweets, then those tweets are checked with our trained model for their classfication either relevant or irrelevant to a disaster and atlast an alert is generated if it matches the requried threshold.</div>"
		,unsafe_allow_html=True)
		st.write("\n")
		st.write("\n")
		col2.markdown("<div style='text-align: justify;text-justify: auto;filter:alpha(opacity=50); opacity:0.7;' class = 'center'>@User is used to fetch tweets by a specific user from Twitter API. Such users could be anyone on the Twitter that posts tweets related to the disaster of the four types i.e., Earthquake, Flood, Hurricane, and Wildfire.</div>"
		,unsafe_allow_html=True)
		st.write("\n")
		st.write("\n")
		col2.markdown("<div style='text-align: justify;text-justify: auto;filter:alpha(opacity=50); opacity:0.7;' class = 'center'>Twitter API is used to either extract tweets related to a specific hashtag,user or you can let the system search for a specific tags and regions The Twitter API will fetch the most recent tweets.</div>"
		,unsafe_allow_html=True)

	# For User Input
	elif selected == "User Input":

		st.markdown("<h1 style='text-align: center; color: #00acee;'>Analysis Of Tweets For User Input</h1>", unsafe_allow_html=True)
		
		lottie_user = load_lottiefile('D:\\Study\\FYP\\app\\animations\\type.json')

		st_lottie(lottie_user, loop=True,speed=1, reverse=False,width=500, height=400)
		txt = st.text_input("Write tweet")
		btn = st.button("Submit")
		if btn:
			if len(txt) == 0:
				st.error("Invalid Input")

			else:
				with st.spinner(text="In progress..."):
        
					txt = do_process_eng_hashtag(txt)
					result = liveExample(modelObj, txt,"LR")

					if result == "Relevant_Tweet":
						st.write("*Tweet :*",txt)
						st.write("Pre-processed: ",prep(txt))
						st.write('*Results :*',result)
						image = Image.open('D:\\Study\\FYP\\app\\Pictures\\sad1.png')
						st.image(image, caption='The Tweet is related to Disaster',width = 200)
					else:
						st.write("*Tweet :*",txt)
						st.write("Pre-processed: ",prep(txt))
						st.write('*Results :*',result)
						image = Image.open('D:\\Study\\FYP\\app\\Pictures\\happy1.png')
						st.image(image, caption='The Tweet is not related to Disaster',width = 200)
				st.success('done.!')



	# For Twitter API
	elif selected == "Import From Twitter API":

		api = tweepy.API(api_access())


		sel = st.sidebar.selectbox("Select Input Method By", ("-","@User", "#Hashtag","Automated Search"))

		if sel == "-":

			st.markdown("<h1 style='text-align: left; color: #00acee;'>Analysis Of Tweets From Twitter API \n</h1>", unsafe_allow_html=True)
			st.write("\n")

			
			col1,col2 = st.columns(2)
			with col2:
				lottie_API = load_lottiefile('D:\\Study\\FYP\\app\\animations\\API_back.json')
				st_lottie(lottie_API, loop=True,speed=1, reverse=False,width=300, height=350)

			with col1:
				st.markdown("<div style='text-align: justify;text-justify: auto;filter:alpha(opacity=50); opacity:0.7;' class = 'center'>Analysis refers to identifying as well as classifying the opinions that are expressed in the text source. Tweets are often useful in generating a vast amount of sentiment data upon analysis. These data are useful in understanding the opinion of the people about a variety of topics. Therefore we need to develop an Automated Machine Learning analysis Model in order to compute the customer perception. Due to the presence of non-useful characters (collectively termed as the noise) along with useful data, it becomes difficult to implement models.</div>", unsafe_allow_html=True)
			st.write("\n")

			# API access function call


		elif sel == "@User":

			st.markdown("<h2 style='text-align: center; color: #00acee ;'>Analysis Of Tweets From Specific User\n</h2>", unsafe_allow_html=True)			
			st.write("\n")
			st.write("\n")

			st.info("Input a valid @User")
			st.write("\n")

			txt1 = st.text_input("Write @User name")
			st.write("e.g, @User_name")
			st.write("\n")
			btn1 = st.button("Submit")

			if btn1:
				if len(txt1) == 0:
					st.error("Invalid Input")

				else:
					if txt1.startswith('@'):
						key = txt1
						by_User_Hashtags(key)
					else:
						st.error("Invalid Input")
				st.success('Done.')


		elif sel == "#Hashtag":

			st.markdown("<h2 style='text-align: center; color: #00acee ;'>Analysis Of Tweets Using Hashtags\n</h2>", unsafe_allow_html=True)			
			st.write("\n")
			st.write("\n")

			st.info("Input a valid #Hashtag")
			st.write("\n")

			txt2 = st.text_input("Write hashtag/hashtags")
			st.write("e.g, #earthquake OR #UnitedStates")
			st.write("\n")
			btn1 = st.button("Submit")
			if btn1:
				if len(txt2) == 0:
					st.error("Invalid Input")

				else:
					if txt2.startswith('#'):
						
						key = txt2 + " -filter:retweets"
						by_User_Hashtags(key)


							#st.subheader("------ All done ------")

					else:
						st.error("Invalid Input")
				st.success('Done.')
    
		# Automated Search
		elif sel == "Automated Search":
			st.markdown("<h2 style='text-align: center; color: #00acee ;'>Analysis Of Tweets By Disaster Type And Specific Region\n</h2>", unsafe_allow_html=True)			
			st.write("\n")
			st.write("\n")

			tags = ["#Earthquake","#Hurricane","#Flood","#Wildfire"]

			side = st.selectbox("Select Type of Disaster",("-", "Earthquake", "Hurricane","Flood","Wildfire"))

			
			# Earthquake
			if side == "Earthquake":
				quakes = st.selectbox("Select Region", ("-","UnitedStates","California","Alaska","Nevada","Hawaii","Montana"))
				lst = ["-","UnitedStates","California","Alaska","Nevada","Hawaii","Montana"]
				if quakes == "UnitedStates":
					key = tags[0] + f" OR #{lst[1]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif quakes == "California":
					key = tags[0] + f" OR #{lst[2]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif quakes == "Alaska":
					key = tags[0] + f" OR #{lst[3]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif quakes == "Nevada":
					key = tags[0] + f" OR #{lst[4]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif quakes == "Hawaii":
					key = tags[0] + f" OR #{lst[5]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif quakes == "Montana":
					key = tags[0] + f" OR #{lst[6]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')
			
			# Hurricane
			elif side == "Hurricane":
				huricane = st.selectbox("Select region ",("-","Florida","Texas","NorthCarolina","Louisiana"))
				lst2 = ["-","Florida","Texas","NorthCarolina","Louisiana"]

				if huricane == "Florida":
					key = tags[1] + f" OR #{lst2[1]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif huricane == "Texas":
					key = tags[1] + f" OR #{lst2[2]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif huricane == "NorthCarolina":
					key = tags[1] + f" OR #{lst2[3]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif huricane == "Louisiana":
					key = tags[1] + f" OR #{lst2[4]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

			# Flood
			if side == "Flood":
				flod = st.selectbox("Select Region", ("-","Georgia","Massachusetts","NorthCarolina","Virginia","SouthCarolina","NewJersey"))
				lst3 = ["-","Georgia","Massachusetts","NorthCarolina","Virginia","SouthCarolina","NewJersey"]
				if flod == "Georgia":
					key = tags[2] + f" OR #{lst3[1]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif flod == "Massachusetts":
					key = tags[2] + f" OR #{lst3[2]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif flod == "NorthCarolina":
					key = tags[2] + f" OR #{lst3[3]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif flod == "Virginia":
					key = tags[2] + f" OR #{lst3[4]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif flod == "SouthCarolina":
					key = tags[2] + f" OR #{lst3[5]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif flod == "NewJersey":
					key = tags[2] + f" OR #{lst3[6]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')


				
			# Wildfire
			if side == "Wildfire":
				wildfir = st.selectbox("Select Region", ("-","Alaska","Arizona","California","Colorado","Idaho","Montana"))
				lst4 = ["-","Alaska","Arizona","California","Colorado","Idaho","Montana"]
				if wildfir == "Alaska":
					with st.spinner(text="In progress..."):				
						key = tags[3] + f" OR #{lst4[1]} -filter:retweets"
						automatic_search(key)
					st.success('done.!')

				elif wildfir == "Arizona":
					key = tags[3] + f" OR #{lst4[2]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif wildfir == "California":
					key = tags[3] + f" OR #{lst4[3]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif wildfir == "Colorado":
					key = tags[3] + f" OR #{lst4[4]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif wildfir == "Idaho":
					key = tags[3] + f" OR #{lst4[5]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

				elif wildfir == "Montana":
					key = tags[3] + f" OR #{lst4[6]} -filter:retweets"
					automatic_search(key)
					st.success('done.!')

			
			
			

		else:
			st.error("Invalid Input")


else:
    
	header("DATASET\n")
	st.text("\n")
	st.text("\n")

	st.write("\n")
	st.markdown("<div style='text-align: justify;text-justify: auto;filter:alpha(opacity=50); opacity:0.7;' class = 'center'>The following section contains the dataset acquired for making a trained model for the prediction and classification of tweets. The subsequent below results are from the Initial dataset and Preprocessed dataset on which the machine learning classifiers were used to train a model. Furthermore, the beneath graphs are an easy illustration of the dataset, the data inside the dataset, the accuracy and F1 score of the models.</div>"
	,unsafe_allow_html=True)
	st.write("\n")
	st.write("\n")


	df1 = pd.read_csv('D:\\Study\\FYP\\app\\Datasets\\InitialDataset.csv')
	df1 = df1.sample(frac=1).reset_index()
	Subheader("The Initial Dataset Dataset :")
	st.write("\n")
	st.write("Total dataset Length:",df1.shape[0])
	st.write("\n")
	st.write(df1)	


	df2 = pd.read_csv('D:\\Study\\FYP\\app\\Datasets\\preprocessed.csv')
	Subheader("The Preprocessed Dataset :")
	st.write("\n")
	st.write("Total dataset Length after duplicate and Null removal:",df2.shape[0])
	st.write("\n")
	st.write(df2)	

	img1 = Image.open("D:\\Study\\FYP\\app\\Pictures\\img1.png")
	img2 = Image.open("D:\\Study\\FYP\\app\\Pictures\\img2.png")
	img3 = Image.open("D:\\Study\\FYP\\app\\Pictures\\img3.png")
	img4 = Image.open("D:\\Study\\FYP\\app\\Pictures\\img4.png")
	img5 = Image.open("D:\\Study\\FYP\\app\\Pictures\\img5.png")


	img6 = Image.open("D:\\Study\\FYP\\app\\Pictures\\LR1.png")
	img7 = Image.open("D:\\Study\\FYP\\app\\Pictures\\LR2.png")
	img8 = Image.open("D:\\Study\\FYP\\app\\Pictures\\RF1.png")
	img9 = Image.open("D:\\Study\\FYP\\app\\Pictures\\RF2.png")
	img10 = Image.open("D:\\Study\\FYP\\app\\Pictures\\DT1.png")

	img11 = Image.open("D:\\Study\\FYP\\app\\Pictures\\DT2.png")
	img12 = Image.open("D:\\Study\\FYP\\app\\Pictures\\LSVC1.png")
	img13 = Image.open("D:\\Study\\FYP\\app\\Pictures\\LSVC2.png")
	img14 = Image.open("D:\\Study\\FYP\\app\\Pictures\\SVM1.png")
	img15 = Image.open("D:\\Study\\FYP\\app\\Pictures\\SVM2.png")

	img16 = Image.open("D:\\Study\\FYP\\app\\Pictures\\GB1.png")
	img17 = Image.open("D:\\Study\\FYP\\app\\Pictures\\GB2.png")
	img18 = Image.open("D:\\Study\\FYP\\app\\Pictures\\rela.png")




	exp = st.expander(label = "EXPLORE DATASET")
	with exp:

		st.write('\n')
		st.write('\n')
		exp.subheader("Disaster Related and Not-Related Ratio")
		st.write('\n')
		exp.image(img18)

		st.write('\n')
		st.write('\n')
		exp.subheader("Plotation as Sum of All Most Frequent Words ")
		st.write('\n')
		exp.image(img1)

		st.write('\n')
		st.write('\n')
		exp.subheader("Plotation as Sum of All Positive Frequent Words ")
		st.write('\n')
		st.image(img3)

		st.write('\n')
		st.write('\n')
		exp.subheader("Plotation as Sum of All Negative Frequent Words ")
		st.write('\n')
		st.image(img2)

		st.write('\n')
		st.write('\n')
		exp.subheader("Plotation of top 10 Positive Hashtags ")
		st.write('\n')
		st.image(img4)
		
		st.write('\n')
		st.write('\n')
		exp.subheader("Plotation of top 10 Negative Hashtags ")
		st.write('\n')
		st.image(img5)

	
	exp1 = st.expander(label = "VIEW TRAINED MODELS")
	with exp1:
		st.write('\n')
		st.write('\n')
		exp1.subheader("LOGISTIC REGRESSION ")
		st.write('\n')
		exp1.image(img6)

		st.write('\n')
		exp1.image(img7)


		st.write('\n')
		st.write('\n')
		exp1.subheader("RANDOM FOREST ")
		st.write('\n')
		exp1.image(img8)

		st.write('\n')
		exp1.image(img9)


		st.write('\n')
		st.write('\n')
		exp1.subheader("DECISION TREE")
		st.write('\n')
		exp1.image(img10)

		st.write('\n')
		exp1.image(img11)

		st.write('\n')
		st.write('\n')
		exp1.subheader("Linear SVC ")
		st.write('\n')
		exp1.image(img12)

		st.write('\n')
		exp1.image(img13)


		st.write('\n')
		st.write('\n')
		exp1.subheader("SUPPORT VECTOR MACHINE (SVM) ")
		st.write('\n')
		exp1.image(img14)

		st.write('\n')
		exp1.image(img15)

		st.write('\n')
		st.write('\n')
		exp1.subheader("GRADIENT BOOSTING ")
		st.write('\n')
		exp1.image(img16)

		st.write('\n')
		exp1.image(img17)

	




	

