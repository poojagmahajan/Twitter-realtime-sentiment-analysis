# Import necessary libraries

import tweepy
from textblob import TextBlob
from tweepy import OAuthHandler
import csv
import re
import twitter_credentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse


# TWITTER AUTHENTICATOR
class TwitterAuthenticator():
    # Class constructor or initialization method.
    def __init__( self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET ):
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            # set access token and secret
            self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        except:
            print("Error: Authentication Failed")

    # method to access OAuthHandler object
    def get( self ):
        return self.auth


# # # # TWITTER CLIENT # # # #
class TwitterClient():

    def __init__( self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET ):
        # create object of TwitterAuthenticator class
        self.twitter_authenticator = TwitterAuthenticator(CONSUMER_KEY, CONSUMER_SECRET,
                                                          ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        #  access OAuthHandler object
        self.auth = self.twitter_authenticator.get()

        # create tweepy API object to fetch tweets
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

    # method to access client api
    def get_twitter_client_api( self ):
        return self.api

    # method to fetch tweets of hashtaglist between specific duration of geocode of India
    def get_data( self, my_hashtag_list, my_since, my_geocode, my_until, my_lang, my_count ):
        data = tweepy.Cursor(self.api.search, q=my_hashtag_list,
                             since=my_since, geocode=my_geocode,
                             until=my_until, lang=my_lang, count=my_count)
        return data


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    # clean tweets using regex function(removing hyperlink, #, RT, @mentions,numbers,lowercase,special characters)
    def clean_tweet( self, tweet ):
        tweet = ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(\@\w+|\#)|("
                                r"http\S+|www\S+|https\S+)|(^RT[\s]+)", " ", tweet).split())
        return tweet

    # method to take data in dataframe
    def tweets_to_data_frame( self, filename ):
        df = pd.read_csv(filename, sep=None, engine='python')
        return df

    # method to calculate sentiment polarity of clean tweets using Textblob's sentiment method
    def analyze_sentiment( self, tweet ):
        # create object for Textblob method
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiments by polarity
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def calculate_percentage( self, number_of_tweets, total_tweets ):

        return 100 * number_of_tweets / total_tweets

    # method to plot sentiments of hashtag we provide
    def visualization( self, sentiments, hashtag ):
        # initialize variables
        positive_tweets = 0
        negative_tweets = 0
        neutral_tweets = 0
        total_tweets = 0
        # increment count of tweets as per sentiments
        for sentiment in sentiments:
            if sentiment == 'positive':
                positive_tweets += 1
            elif sentiment == 'negative':
                negative_tweets += 1
            elif sentiment == 'neutral':
                neutral_tweets += 1
            total_tweets += 1
        # print tweets as per sentiments
        print('positive_tweets :', positive_tweets,
              'negative_tweets :', negative_tweets,
              'neutral_tweets :', neutral_tweets,
              'total_tweets  :', total_tweets)

        # print percentages of sentiments
        print("Positive tweets percentage: {} %".format(self.calculate_percentage(positive_tweets, total_tweets)))
        print("Negative tweets percentage: {} %".format(self.calculate_percentage(negative_tweets, total_tweets)))
        print("Neutral tweets percentage: {} %".format(self.calculate_percentage(neutral_tweets, total_tweets)))

        # plot piechart using matplotlib.plt
        labels = 'positive_tweets', 'negative_tweets', 'neutral_tweets'
        sizes = [self.calculate_percentage(positive_tweets, total_tweets),
                 self.calculate_percentage(negative_tweets, total_tweets),
                 self.calculate_percentage(neutral_tweets, total_tweets)]

        fig1, ax1 = plt.subplots()  # plot output on chart
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Twitter_sentiment_analysis of \n' + str(hashtag) + '\n hashtags')

        plt.show()  # display chart


# method to take arguments from command line using
def parsearguments():
    # Construct the argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument("-H", "--hashtag_list", type=str, help='comma seperated list of hashtags to analyse',
                        required=True)
    parser.add_argument("-s", "--since_date", type=str, help='since date', required=True)
    parser.add_argument("-u", "--until_date", type=str, help='until date', required=True)
    parser.add_argument("-g", "--geocode", help='geocode of india', default="20.5937,78.9629,3000km")
    parser.add_argument("-l", "--language", help='language of tweets', default="en")
    parser.add_argument("-f", "--file", type=str, help='filename to store tweets', required=True)
    parser.add_argument("-c", "--count", type=int, help='no.of tweets required', required=True)

    return parser.parse_args()


if __name__ == '__main__':

    args = parsearguments()

    # construct hashtag_list
    hashtag_list = [item for item in args.hashtag_list.split(',')]

    # create object of TwitterClient class
    twitter_client = TwitterClient(twitter_credentials.CONSUMER_KEY,
                                   twitter_credentials.CONSUMER_SECRET,
                                   twitter_credentials.ACCESS_TOKEN,
                                   twitter_credentials.ACCESS_TOKEN_SECRET)
    # create object of TweeterAnalyzer class
    tweet_analyzer = TweetAnalyzer()

    # Open/create a file to append data to
    filename = args.file  # default filename
    # add file extention if required
    if '.csv' not in filename:
        filename = filename + '.csv'

    csvFile = open(filename, 'w')  # open csv with write mode
    csvWriter = csv.writer(csvFile)
    # declare columns to add as header to csv file
    columns = ['date', 'id', 'tweets', 'source', 'truncated', 'retweet_count', 'user_id', 'user_name',
               'user_screen_name', 'geo', 'user_description', 'user_url', 'language']

    # use DictWriter of csv to add columns as fieldnames
    writer = csv.DictWriter(csvFile, fieldnames=columns)
    writer.writeheader()  # pass columns as header of file

    # dictionary to store unique tweets
    unique_tweets = {}
    # declare keywords to search tweets in hashtag-list
    # hashtag_list = ["Sushant Singh Rajput", "#JusticeforSushantSingRajput"]

    for tweet in twitter_client.get_data(my_hashtag_list=hashtag_list,
                                         my_since=args.since_date,
                                         my_geocode=args.geocode,
                                         my_until=args.until_date,
                                         my_lang=args.language,
                                         my_count=args.count).items(args.count):
        # only unique tweets
        if tweet.text not in unique_tweets:
            unique_tweets[tweet.text] = 1
            # write tweets one by one in a file
            csvWriter.writerow([tweet.created_at,
                                str(tweet.id),
                                tweet_analyzer.clean_tweet(tweet.text),
                                tweet.source,
                                tweet.truncated,
                                tweet.retweet_count,
                                tweet.user.id,
                                tweet.user.name,
                                tweet.user.screen_name,
                                tweet.user.location,
                                tweet.user.description,
                                tweet.user.url,
                                tweet.lang])
    # close file
    csvFile.close()
    # call tweets_to_data_frame function
    df = tweet_analyzer.tweets_to_data_frame(filename)
    # add column for sentiments
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    # call to visualization function
    tweet_analyzer.visualization(df['sentiment'], hashtag=hashtag_list)
