#!/usr/bin/env python3
"""
Module Docstring
A scraper for locations based on latitude, longitude, and radius
for twitter. 
"""

__author__ = "Tim Seifert"
__version__ = "0.1.0"
__license__ = "N/A"


import config
import tweepy
import pandas as pd
import json
from translate import Translator

#hiding api keys
auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
translator= Translator(to_lang="en")


#Create list for column names
COLS = ['id','created_at','lang','original text','user_name', 'place', 'place type', 'bbx', 'coordinates']

geo='9.148086,40.49305,800km'
since_date='2020-02-10'
until_date='2021-02-10'
max_pages = 500
#Credit goes to https://stackoverflow.com/questions/62101893/python-tweepy-get-all-tweets-based-on-geocode for the solution of how to use tweepy with geo-codes!
#The Twitter Search API searches against a sampling of recent Tweets published in the past 7 days. 
def write_tweets(keyword):

    #create dataframe from defined column list
    df = pd.DataFrame(columns=COLS)

    #iterate through pages with given condition
    #using tweepy.Cursor object with items() method
    for page in tweepy.Cursor(api.search,q=keyword,since_id=2020, include_rts=False,
                                  geocode=geo).pages(max_pages):

                for tweet in page:
                    #creating string array
                    new_entry = []

                    #storing all JSON data from twitter API
                    tweet = tweet._json 

					#make use of the translator ?


                    #Append the JSON parsed data to the string list:
					
                    new_entry += [tweet['id'], tweet['created_at'], tweet['lang'], tweet['text'], 
                                  tweet['user']['name']]

                    #check if place name is available, in case not the entry is named 'no place'
                    try:
                        place = tweet['place']['name']
                    except TypeError:
                        place = 'no place'
                    new_entry.append(place)

                    try:
                        place_type = tweet['place']['place_type']
                    except TypeError:
                        place_type = 'na'
                    new_entry.append(place_type)

                    try:
                        bbx = tweet['place']['bounding_box']['coordinates']
                    except TypeError:
                        bbx = 'na'
                    new_entry.append(bbx)

                    #check if coordinates is available, in case not the entry is named 'no coordinates'
                    try:
                        coord = tweet['coordinates']['coordinates']
                    except TypeError:
                        coord = 'no coordinates'
                    new_entry.append(coord)
					
                    # wrap up all the data into a data frame
                    single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
                    df = df.append(single_tweet_df, ignore_index=True)

                    #get rid of tweets without a place
                    df_cleaned = df[df.place != 'no place']


    print("tweets with place:")
    print(len(df[df.place != 'no place']))

    print("tweets with coordinates:")
    print(len(df[df.coordinates != 'no coordinates']))

    df_cleaned.to_csv('tweets_'+geo+keyword+'.csv', columns=COLS,index=False)

#declare keywords as a query
keyword="#ethiopia"

#call main method passing keywords and file path
write_tweets(keyword)