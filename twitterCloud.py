import os, path
import tweepy
import pandas as pd
import string 
from wordcloud import STOPWORDS, WordCloud, ImageColorGenerator
import imageio
import matplotlib.pyplot as plt
import numpy as np
import PIL
import random
from scipy.ndimage import gaussian_gradient_magnitude

## Note: the user input, csvFileName input, imageName input, and imageCloudFileName must all be strings.

## For the wordstoAdd input, just enter the words as a continuous string separated by commas ("wordone wordtwo wordthree") in 
## all lowercase


## For authentication, enter your Twitter Developer credentials in the appropriate variables below

auth = tweepy.OAuthHandler('','')
auth.set_access_token('','')
api = tweepy.API(auth)

## Note: the user input, csvFileName input, imageName input, and imageCloudFileName must all be strings.

## For the wordstoAdd input, just enter the words as a continuous string separated by commas ("wordone wordtwo wordthree") in 
## all lowercase

def pullTweets(user, count, csvFileName, imageName, imageCloudFileName):
   
    userTweets = []


    for i in tweepy.Cursor(api.user_timeline, id = user, tweet_mode = 'extended').items(count):
        userTweets.append(i.full_text)
        userDf = pd.DataFrame({'tweets': userTweets})
        curDir = os.getcwd()
        userDf.to_csv(r'{}\{}'.format(curDir,csvFileName))
    STOP = set(STOPWORDS)
    wordstoAdd = input("enter the list of words to add to the current stopwords list: ")
    sepWords = wordstoAdd.split()
    for i in range(len(sepWords)):
        STOP.add(sepWords[i])
    
    def text_processing(mess):
        
        nopunc = [char for char in mess if char not in string.punctuation]
    
        nopunc = ''.join(nopunc)
        
    
        return [word for word in nopunc.split() if word.lower() not in STOP]   
        
    
    noStopWords = np.concatenate(np.array(userDf['tweets'].apply(text_processing)), axis = 0)
    image_color = np.array(PIL.Image.open(r'{}\{}'.format(curDir, imageName)))
    image_color = image_color[::3, ::3]
    image_mask = image_color.copy()
    image_mask[image_mask.sum(axis=2) == 0] = 255
    edges = np.mean([gaussian_gradient_magnitude(image_color[:, :, i] / 255., 2) for i in range(3)], axis = 0)
    image_mask[edges > 0.08] = 255
    Words = ' '.join([str(elem) for elem in noStopWords])
    wc = WordCloud(max_words = 1000, mask = image_mask, margin = 1,
               random_state = 1, relative_scaling = 0).generate(Words)
    colors = ImageColorGenerator(image_color)
    

    finalWC = plt.imshow(wc.recolor(color_func=colors, random_state = 3),
        interpolation = "bilinear")
    plt.axis("off")
    plt.savefig(r'{}\{}'.format(curDir, imageCloudFileName), dpi=300)
    return finalWC

 ## Example
 ## to Pull 1000 tweets from Barack Obama's profile, the following function is used
 ## Note: the being used for the word cloud mask must be in the current working directory
  
pullTweets('barackobama', 1000, 'barack.csv', 'Obama.png', 'ObamaCloud.png')
  
  
