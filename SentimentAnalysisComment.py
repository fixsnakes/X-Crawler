from XAuth import XCrawler
import pandas as pd



#https://x.com/realDonaldTrump/status/1851469982145663300


idPost = "1854072387722989629"

cookie = ''

Xobj = XCrawler("username","password",cookie)


DataCommentTweet = Xobj.GetCommentOfTweet(idPost)



#Sentiment Tweet
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import string,re


from pathlib import Path
filepath = f"Sentiment Tweet Data\\{idPost}"
folder_path = Path(filepath)
def SentimentTweet(tweet):

    
    
    stopwordlist = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an',
             'and','any','are', 'as', 'at', 'be', 'because', 'been', 'before',
             'being', 'below', 'between','both', 'by', 'can', 'd', 'did', 'do',
             'does', 'doing', 'down', 'during', 'each','few', 'for', 'from',
             'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here',
             'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in',
             'into','is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma',
             'me', 'more', 'most','my', 'myself', 'now', 'o', 'of', 'on', 'once',
             'only', 'or', 'other', 'our', 'ours','ourselves', 'out', 'own', 're','s', 'same', 'she', "shes", 'should', "shouldve",'so', 'some', 'such',
             't', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them',
             'themselves', 'then', 'there', 'these', 'they', 'this', 'those',
             'through', 'to', 'too','under', 'until', 'up', 've', 'very', 'was',
             'we', 'were', 'what', 'when', 'where','which','while', 'who', 'whom',
             'why', 'will', 'with', 'won', 'y', 'you', "youd","youll", "youre",
             "youve", 'your', 'yours', 'yourself', 'yourselves']


    STOPWORDS = set(stopwordlist)
    def PreprocessData(text):
        english_punctuations = string.punctuation
        punctuations_list = english_punctuations
        text =  " ".join([word for word in str(text).split() if word not in STOPWORDS and "@" not in word and len(word) > 3 and "http" not in word])
        translator = str.maketrans('', '', punctuations_list)
        text = text.translate(translator)

        text = re.sub(r'(.)1+', r'1', text)
        
        text = re.sub('((www.[^s]+)|(https?://[^s]+))',' ',text)
    
        text =  re.sub('[0-9]+', '', text)
        
        text = re.sub(r'[^A-Za-z\s]', '', text)
        return text


    tweet_proc = PreprocessData(tweet)
    
   
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"

    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    labels = ['Negative', 'Neutral', 'Positive']

    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')


    output = model(**encoded_tweet)

    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    
    max_ss = 0
    max_label = ''
    

    for i in range(len(scores)):
        
        l = labels[i]
        s = scores[i]
        
        if(float(s) > max_ss):
            max_ss = s
            max_label = l
    
    return max_label



folder_path.mkdir(parents=True, exist_ok=True)

pos = 0
neg = 0
neutral = 0

for data in DataCommentTweet:
    print(data)
    
    sentiment = SentimentTweet(data['content'])
    print(sentiment)
    
    data['sentiment'] = sentiment
    if sentiment == 'Positive':
        pos += 1
    elif sentiment == 'Negative':
        neg += 1
    else:
        neutral += 1
        



from openpyxl import load_workbook

import matplotlib.pyplot as plt

df = pd.DataFrame(DataCommentTweet, columns=['user', 'content', 'like', 'sentiment'])


df.columns = ['User', 'Content', 'Like', 'Sentiment']


pathfinal = f"{filepath}\\datadetail.xlsx"


df.to_excel(pathfinal,index=False)

labels = ['Positive', 'Negative', 'Neutral']
sizes = [pos, neg, neutral] 
colors = ['#66b3ff', '#ff6666', '#ffcc99']  


plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.title('Sentiment Data')
plt.savefig(f'{filepath}\\sentimentChart.png')
plt.show()



    