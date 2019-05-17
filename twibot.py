#!/usr/bin/python3.6
import os
import datetime
import random
import tweepy
import psycopg2

def main():
    tweet_word = get_my_tweet()
    
    auth =  tweepy.OAuthHandler(os.environ['consumer_key'], os.environ['consumer_secret'])
    auth.set_access_token(os.environ['access_token'], os.environ['access_token_secret'])
    api = tweepy.API(auth_handler=auth)

    api.update_status(tweet_word)

def get_my_tweet():
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    n_time = datetime.datetime.now(JST)
    n_hour = n_time.strftime('%H')

    conn = db_connect()
    sql = "SELECT tweet FROM tw_post WHERE display=True;"
    with conn.cursor() as cur:
        cur.exectute(sql)
        result = cur.fetchall()

    tweets = []
    for row in result:
        tw_str = row[0]
        while len(tw_str.encode('utf-8')) > 132:
            tw_str = tw_str[:-1]
        tw = {
            'tweet_word': tw_str + '(' + str(n_hour) + ')'
        }
        tweets.append(tw)

    tweet_word = random.choice(tweets)
    return tweet_word

def db_connect():
    pg_url = os.environ['pg_url']
    conn = psycopg2.connect(pg_url)
    return conn

if __name__ == '__main__':
    main()