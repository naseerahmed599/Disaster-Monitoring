import streamlit as st
from alert import *
import tweepy
from UserInput import *
from twitter_api import *

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px


from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score

import warnings
warnings.filterwarnings("ignore")


def Subheader(url):
    st.markdown(f'<p style="color:#00acee ;font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def info_df(url):
    st.markdown(f'<p style="color:#00acee ;font-size:22px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def bold_text(url):
     st.markdown(f"<h3 style='text-align: center;border-radius:2%;color: red;'>{url}</h3>", unsafe_allow_html=True)

def do_process_eng_hashtag(input_text: str) -> str:
    return re.sub(
        r'#[a-z]\S*',
        lambda m: ' '.join(re.findall('[A-Z][^A-Z]*|[a-z][^A-Z]*', m.group().lstrip('#'))),
        input_text,
    )


def automatic_search(key):
    # Search by Keyword or Hashtag
    with st.spinner(text="In progress..."):
        info_df("\n --- Extracting Tweets ---\n")
        api = tweepy.API(api_access())
        
        keyword = key

        st.write("Checking :", keyword)

        limit = 300

        tweets = tweepy.Cursor(api.search_tweets,q = keyword, count = 100, tweet_mode = 'extended', lang = 'en').items(limit)

        # Create Dataframe
        columns = ['User','tweets']
        data = []

        for tweet in tweets:
            data.append([tweet.user.screen_name, tweet.full_text])


        df = pd.DataFrame(data, columns = columns)
        st.write("\n")
        info_df("--- Tweets extraction done ---")
        st.write("-------------------")

        st.write("\n")
    
    with st.spinner(text="In progress..."):
        info_df("\n --- Preprocessing Tweets ---\n")
        st.write("-------------------")
        # Hashtag Extract
        df['hashtags'] = hashtags_extract(df['tweets'])
        
        # Split multi-word hashtag in python
        df['clean_tweet'] = df['tweets'].apply(lambda tweet: do_process_eng_hashtag(tweet))


        # Preprocessing
        df['clean_tweet'] = df['tweets'].apply(lambda tweet: pre_tweet_API(tweet))
        

        # Drop Duplicate and Null
        df["clean_tweet"] =df["clean_tweet"].drop_duplicates()
        df = df.dropna()
        info_df("\n --- Preprocessing done ---\n")
        st.write("-------------------")


    with st.spinner(text="In progress..."):
        info_df("\n --- Checking with Model ---\n")
        st.write("-------------------")

        # Use Trained Model
        df['predicted'] = df['clean_tweet'].apply(lambda tweet: twitter_live_exp(modelObj,tweet,"LR"))
        df['relevance'] = df['clean_tweet'].apply(lambda tweet: twitter_live_exp_sent(modelObj,tweet,"LR"))


        #plt.figure(figsize=(7, 7))
        #fig1 = plt.pie(df['Relevance'].value_counts(),labels=[1,0],autopct='%0.2f')
        #st.pyplot(fig1)

        info_df("The Initial Dataframe of Tweets")
        st.write(df[["User","tweets"]])

        info_df("The Post Dataframe of Tweets")
        st.write(df[["hashtags","clean_tweet","predicted","relevance"]])
 
        st.write("The Irrelevance column (0) :",int(df.loc[df['predicted'] == 0].shape[0]))
        st.write("The Relevant column (1) :",int(df.loc[df['predicted'] == 1].shape[0]))
        
        tot = int(df['predicted'].shape[0])
        rel = int(df.loc[df['predicted'] == 1].shape[0])
        

        exp = st.expander(label = "EXPLORE IMPORTED DATASET")
        with exp:

            if len(df) == 0:
                st.write("\nThe Dataframe is Empty. \n")
            
            else:
                #The plot
                tweet_cnt = df.groupby(by=["relevance"]).count()[['predicted']].rename(columns={"predicted":"Count"}).reset_index()
                fig = px.pie(tweet_cnt, values='Count', names='relevance', title='Tweets Distribution')

                st.header("Pie chart")
                st.plotly_chart(fig)
                
                
                
                
                st.subheader("Plotation as Sum of All Most Frequent Words")


                # visualize the frequent words
                all_words = " ".join([sentence for sentence in df['tweets']])

                from wordcloud import WordCloud
                wordcloud = WordCloud(width = 800, height=500, random_state=42, max_font_size=100, background_color='white').generate(all_words)

                # plot the graph
                plt.figure(figsize=(15,8))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                fig2 = plt.show()
                st.pyplot(fig2)

                if int(df.loc[df['predicted'] == 1].shape[0]) == 0:
                    st.write("\nThere is no relevant tweets to disaster.\n")
                
                else:								
                    st.subheader("Plotation of Related Most Frequent Words")
                    # frequent word visualization for Positive
                    all_words = " ".join([sentence for sentence in df['tweets'][df['predicted']==1]])

                    from wordcloud import WordCloud
                    wordcloud = WordCloud(width = 800, height=500, random_state=42, max_font_size=100).generate(all_words)

                    # plot the graph
                    plt.figure(figsize=(15,8))
                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis('off')
                    fig3 = plt.show()
                    st.pyplot(fig3)

                if int(df.loc[df['predicted'] == 0].shape[0]) == 0:
                    st.write("\nThere is no irrelevant tweets to disaster.\n")
                
                else:
                                                
                    st.subheader("Plotation of Not-Related Most Frequent Words")
                    st.write(len(df['predicted'] == 0))

                    # frequent word visualization for Negative
                    all_words = " ".join([sentence for sentence in df['tweets'][df['predicted']==0]])

                    from wordcloud import WordCloud
                    wordcloud = WordCloud(width = 800, height=500, random_state=42, max_font_size=100).generate(all_words)

                    # plot the graph
                    plt.figure(figsize=(15,8))
                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis('off')
                    fig4 = plt.show()
                    st.pyplot()


        if int(df.loc[df['predicted'] == 0].shape[0]) != 0 and int(df.loc[df['predicted'] == 1].shape[0]) != 0:
            
            tot_df_len = int(df.shape[0])
            irrel = int(df.loc[df['predicted'] == 0].shape[0])
            rel = int(df.loc[df['predicted'] == 1].shape[0])
            irrel_av = (irrel*100)/tot_df_len
            irrel_av = int(irrel_av)
            st.write("Irrelevant-Tweets Percentage:",irrel_av,"% out of 100 %")

            rel_av = (rel*100)/tot_df_len
            rel_av = int(rel_av)
            st.write("Relevant-Tweets Percentage:",rel_av,"% out of 100 %")

            
            if rel > 20:
                if rel_av >= 50:
                    if rel_av == 50:
                        st.text("Pecentage of the Relevant Tweets is 50%")
                    else:
                        st.text("Pecentage of the Relevant Tweets is above 50%")
                    st.text("Sending Alert.....")
                    email_alert(keyword,f'Warning, Out of {tot_df_len} tweets, {rel} number of tweets are Related to Disaster with the Total percentage of {rel_av}%. Therefore, Action is to be taken.','ahmednaseer5991@gmail.com')
                    info_df("Alert has been sent.")

                else:
                    st.info("Percentage of Relevant Tweet is not satisfactory. \n")
            else:
                info_df("The number of related tweet is less than 20. Therfore, Can not send ALERT.")
        else:
            Subheader("\nCan not proceed with the empty Dataframe. \n")





def by_User_Hashtags(key):
    # Search by Keyword or Hashtag
    with st.spinner(text="In progress..."):
        info_df("\n --- Extracting Tweets ---\n")
        api = tweepy.API(api_access())
        
        keyword = key
        
        st.write("Checking :", keyword)
        
        if keyword.startswith("@"):
            limit = 300
            tweets = tweepy.Cursor(api.user_timeline, screen_name = key, count = 200, tweet_mode = 'extended').items(limit)
        elif keyword.startswith("#"):    
            limit = 300
            tweets = tweepy.Cursor(api.search_tweets,q = keyword, count = 100, tweet_mode = 'extended', lang = 'en').items(limit)

        # Create Dataframe
        columns = ['User','tweets']
        data = []

        for tweet in tweets:
            data.append([tweet.user.screen_name, tweet.full_text])


        df = pd.DataFrame(data, columns = columns)
        st.write("\n")
        info_df("--- Tweets extraction done ---")
        st.write("-------------------")

        st.write("\n")
    
    with st.spinner(text="In progress..."):
        info_df("\n --- Preprocessing Tweets ---\n")
        st.write("-------------------")

        # Hashtag Extract
        df['hashtags'] = hashtags_extract(df['tweets'])
        
        # Split multi-word hashtag in python
        df['clean_tweet'] = df['tweets'].apply(lambda tweet: do_process_eng_hashtag(tweet))


        # Preprocessing
        df['clean_tweet'] = df['tweets'].apply(lambda tweet: pre_tweet_API(tweet))

        # Drop Duplicate and Null
        df["clean_tweet"] =df["clean_tweet"].drop_duplicates()
        df = df.dropna()
        info_df("\n --- Preprocessing done ---\n")
        st.write("-------------------")


    with st.spinner(text="In progress..."):
        info_df("\n --- Checking with Model ---\n")
        st.write("-------------------")

        # Use Trained Model
        df['predicted'] = df['clean_tweet'].apply(lambda tweet: twitter_live_exp(modelObj,tweet,"LR"))
        df['relevance'] = df['clean_tweet'].apply(lambda tweet: twitter_live_exp_sent(modelObj,tweet,"LR"))


        #plt.figure(figsize=(7, 7))
        #fig1 = plt.pie(df['Relevance'].value_counts(),labels=[1,0],autopct='%0.2f')
        #st.pyplot(fig1)

        info_df("The Initial Dataframe of Tweets")
        st.write(df[["User","tweets"]])

        info_df("The Post Dataframe of Tweets")
        st.write(df[["hashtags","clean_tweet","predicted","relevance"]])

 
        info_df("The Irrelevance column (0) :")
        st.write(int(df.loc[df['predicted'] == 0].shape[0]))
        st.write("The Relevant column (1) :")
        st.write(int(df.loc[df['predicted'] == 1].shape[0]))
        
        tot = int(df['predicted'].shape[0])
        rel = int(df.loc[df['predicted'] == 1].shape[0])
        
        

        exp = st.expander(label = "EXPLORE IMPORTED DATASET")
        with exp:

            if len(df) == 0:
                st.write("\nThe Dataframe is Empty. \n")
            
            else:
                tweet_cnt = df.groupby(by=["relevance"]).count()[['predicted']].rename(columns={"predicted":"Count"}).reset_index()
                fig = px.pie(tweet_cnt, values='Count', names='relevance', title='Tweets Distribution')

                st.header("Pie chart")
                st.plotly_chart(fig)


                
                
                st.subheader("Plotation as Sum of All Most Frequent Words")


                # visualize the frequent words
                all_words = " ".join([sentence for sentence in df['tweets']])

                from wordcloud import WordCloud
                wordcloud = WordCloud(width = 800, height=500, random_state=42, max_font_size=100, background_color='white').generate(all_words)

                # plot the graph
                plt.figure(figsize=(15,8))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                fig2 = plt.show()
                st.pyplot(fig2)

                if int(df.loc[df['predicted'] == 1].shape[0]) == 0:
                    st.write("\nThere is no relevant tweets to disaster.\n")
                
                else:								
                    st.subheader("Plotation of Related Most Frequent Words")
                    # frequent word visualization for Positive
                    all_words = " ".join([sentence for sentence in df['tweets'][df['predicted']==1]])

                    from wordcloud import WordCloud
                    wordcloud = WordCloud(width = 800, height=500, random_state=42, max_font_size=100).generate(all_words)

                    # plot the graph
                    plt.figure(figsize=(15,8))
                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis('off')
                    fig3 = plt.show()
                    st.pyplot(fig3)

                if int(df.loc[df['predicted'] == 0].shape[0]) == 0:
                    st.write("\nThere is no irrelevant tweets to disaster.\n")
                
                else:
                                                
                    st.subheader("Plotation of Not-Related Most Frequent Words")
                    st.write(len(df['predicted'] == 0))

                    # frequent word visualization for Negative
                    all_words = " ".join([sentence for sentence in df['tweets'][df['predicted']==0]])

                    from wordcloud import WordCloud
                    wordcloud = WordCloud(width = 800, height=500, random_state=42, max_font_size=100).generate(all_words)

                    # plot the graph
                    plt.figure(figsize=(15,8))
                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis('off')
                    fig4 = plt.show()
                    st.pyplot()


        if int(df.loc[df['predicted'] == 0].shape[0]) != 0 and int(df.loc[df['predicted'] == 1].shape[0]) != 0:	
            							
            tot_df_len = int(df.shape[0])
            irrel = int(df.loc[df['predicted'] == 0].shape[0])
            rel = int(df.loc[df['predicted'] == 1].shape[0])
            irrel_av = (irrel*100)/tot_df_len
            irrel_av = int(irrel_av)
            st.write("Irrelevant-Tweets Percentage:",irrel_av,"% out of 100 %")

            rel_av = (rel*100)/tot_df_len
            rel_av = int(rel_av)
            st.write("Relevant-Tweets Percentage:",rel_av,"% out of 100 %")

            if rel > 20:
                
                if rel_av >= 50:
                    if rel_av == 50:
                        st.text("Pecentage of the Relevant Tweets is 50%")
                    else:
                        st.text("Pecentage of the Relevant Tweets is above 50%")
                    st.text("Sending Alert.....")
                    email_alert(keyword,f'Warning, Out of {tot_df_len} tweets, {rel} number of tweets are Related to Disaster with the Total percentage of {rel_av}%. Therefore, Action is to be taken.','ahmednaseer5991@gmail.com')
                    st.info("Alert has been sent.")

                else:
                    st.info("Percentage of Relevant Tweet is not satisfactory. \n")
            else:
                info_df("The number of related tweet is less than 20. Therfore, Can not send ALERT.")
        else:
            Subheader("\nCan not proceed with the empty Dataframe. \n")
            