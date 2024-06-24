from urlextract import URLExtract
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd
import emoji

# Download NLTK resources (if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')
extractor = URLExtract()

def  fetch_stats(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    
    #1.fetch total number of messages
    
    num_messages = df.shape[0]
    
    #2. number of words
    
    words=[]
    for message in df['message']:
        words.extend(message.split())

    #3. fetch number of media messages
    
    num_media_messages = df[df['message']=="<Media omitted>\n"].shape[0]

    #4. fetch number of links shared
    
    links=[]
    
    for message in df['message']:
        extractor.find_urls(message)
        links.extend(extractor.find_urls(message))
    num_links = len(links)

    return num_messages,len(words),num_media_messages,num_links


def fetch_most_busy_users(df):
    #fetch most busy user
    x = df['user'].value_counts()
    df =  round((df['user'].value_counts()/df.shape[0])*100,2).reset_index()
    df.columns = ['user','percent']
    return x,df

def world_cloud(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=800,height=400,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=' '))
    return df_wc

        
def fetch_most_common_words(selected_user,df):
    #fetch most common words
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df
    

def fecth_emojis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis_list = []
    for message in df['message']:
        emojis_list.extend([c for c in message if c in emoji.EMOJI_DATA.keys()])
    
    emoji_df = pd.DataFrame(Counter(emojis_list).most_common(len(Counter(emojis_list))),columns=['emoji','count'])
    return emoji_df