#!/usr/bin/env python3
"""
Module Docstring
A scraper for locations based on latitude, longitude, and radius
for twitter. 
"""

__author__ = "Tim Seifert"
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


#Create list for column names
COLS = ['id','created_at','lang','original text','user_name', 'place', 'place type', 'bbx', 'coordinates', 'location', 'geo_enabled']
geo='8.9806,38.7578,50km'
since_date='202103082000'
until_date='202104070000'
max_pages = 500
#https://stackoverflow.com/questions/62101893/python-tweepy-get-all-tweets-based-on-geocode 
#The Twitter Search API searches against a sampling of recent Tweets published in the past 7 days. 
def write_tweets(all_words):

    # create dataframe from defined column list
    df = pd.DataFrame(columns=COLS)
    for word in all_words:
    # iterate through pages with given condition
    # using tweepy.Cursor object with items() method
        for page in tweepy.Cursor(api.search, q=word, include_rts=True,
                    fromDate = since_date, toDate= until_date).pages(5000):
                        for tweet in page:
                            #creating string array
                            new_entry = []

                            #storing all JSON data from twitter API
                            tweet = tweet._json 
                            print(tweet)
                            # print(tweet['place']['bounding_box']['coordinates'])

                            #make use of the translator
                            #Append the JSON parsed data to the string list:
                            
                            new_entry += [tweet['id'], tweet['created_at'], tweet['lang'], tweet['text'], 
                                        tweet['user']['name']]

                            #check if place name is available, in case not the entry is named 'no place'
                            place=""
                            try:
                                place = tweet['place']['full_name']
                            except TypeError:
                                place = 'no place'
                            new_entry.append(place)
                            place_type=""
                            try:
                                place_type = tweet['place']['place_type']
                            except TypeError:
                                place_type = 'na'
                            new_entry.append(place_type)
                            bbx=""
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

                            #check if location is available, in case not the entry is named 'no coordinates'
                            try:
                                loc = tweet['user']['location']
                            except TypeError:
                                loc = 'no location'
                            new_entry.append(loc)

                            new_entry.append(tweet['user']['geo_enabled'])
                            
                            
                            single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
                            df = df.append(single_tweet_df, ignore_index=True)
                            
        df.to_csv('tweets_from_ethiopia_en'+word+'.csv', columns=COLS,index=False)




#declare keywords as a query
keyword_en=[]

#grabbing all tweets because we are getting a very low yield
val = 0
for i in range(20):
    longitude = str(round(38.7578+(val/60), 4))
    keyword_en.append("geocode:8.9806,"+longitude+",1mi")
    val += 1

write_tweets(["geocode:8.9806,38.7578,25mi"])
    