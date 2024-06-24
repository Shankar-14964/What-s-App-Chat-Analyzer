import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')
from collections import Counter

st.sidebar.title("Whats App Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # To convert to string
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)
        
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #finding the most busy user
        if selected_user == "Overall":
            st.title("Most Busiest User")
            x,df = helper.fetch_most_busy_users(df)
            x = x.head()
            fig,ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(df)

        #word cloud
        st.title("Word Cloud")
        if selected_user != 'Overall':
            temp = df[df['user']==selected_user]
            wc = helper.world_cloud(selected_user,df)
            fig,ax = plt.subplots()
            ax.imshow(wc,interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

    
        #most common words
        st.title("Most Common Words")
        df = helper.fetch_most_common_words(selected_user,df)
        temp = df[df['user']!='group_notification']
        temp = temp[temp['message']!= '<Media omitted>\n']
        stopwords = set(stopwords.words('english'))
        words=[]
        for message in temp['message']:
            for word in message.lower().split():
                if word not in stopwords:
                    words.append(word)

        most_common_words = Counter(words).most_common(30)
        most_common_words = pd.DataFrame(most_common_words,columns=['word','count'])
        
        fig,ax = plt.subplots()
        ax.bar(most_common_words['word'],most_common_words['count'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #most common emojis
        st.title("Most Common Emojis")
        emoji_df = helper.fecth_emojis(selected_user,df)
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df['count'].head(),labels=emoji_df['emoji'].head(),autopct='%0.2f%%')
            st.pyplot(fig)
        





        
        
        
        

        
        
        


