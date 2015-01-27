#!/usr/bin/env python

import time
from getpass import getpass
from textwrap import TextWrapper
import csv

import tweepy


class StreamWatcherListener(tweepy.StreamListener):

    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
    def on_status(self, status):
        # Open/Create a file to append data
        csvFile = open('tweets.csv', 'a')
        #Use csv Writer
        writer = csv.writer(csvFile)
        try:                    
            print self.status_wrapper.fill(status.text)
            print '\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source)
            writer.writerow([status.author.screen_name, status.created_at, status.text])

        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'


def main():
    # Prompt for login credentials and setup stream object
    """
    consumer_key = raw_input('Consumer Key: ')
    consumer_secret = getpass('Consumer Secret: ')
    access_token = raw_input('Access Token: ')
    access_token_secret = getpass('Access Token Secret: ')
    """
    consumer_key = "M4zmfFuF92BP59Jaux913NuZU"
    consumer_secret = "WieTEE9tAKmC7lNtkqvWEl7esUrgKUMuZHjqtwYSd3eaZsGiEW"
    access_token = "73957988-mfCbCoWX5CN619nz19q4GrckM19y4HpeE1CWkqb35"
    access_token_secret = "1I6YkL14frx4AWsqfN6L4o1HL8xbd3JUahqHnf9G10daE"
    
    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, StreamWatcherListener(), timeout=None)

    # Prompt for mode of streaming
    valid_modes = ['sample', 'filter']
    while True:
        mode = raw_input('Mode? [sample/filter] ')
        if mode in valid_modes:
            break
        print 'Invalid mode! Try again.'

    if mode == 'sample':
        stream.sample(languages = 'en')

    elif mode == 'filter':
        follow_list = raw_input('Users to follow (comma separated): ').strip()
        track_list = raw_input('Keywords to track (comma seperated): ').strip()
        #csvwriter = csv.writer(open("tweets.csv", "a"))

        #stream.filter(languages = ["en"])
        #stream.filter(track = ["basketball"])

        if follow_list:
            follow_list = [u for u in follow_list.split(',')]
            userid_list = []
            username_list = []
            
            for user in follow_list:
                if user.isdigit():
                    userid_list.append(user)
                else:
                    username_list.append(user)
            
            for username in username_list:
                user = tweepy.API().get_user(username)
                userid_list.append(user.id)
            
            follow_list = userid_list
        else:
            follow_list = None
        if track_list:
            track_list = [k for k in track_list.split(',')]
        else:
            track_list = None
        #print follow_list
        #csvwriter.writerow([follow_list])
        #print(track_list[0])
        for i in xrange(5000):
            stream.filter(track= [track_list[0]] ,languages = ["en"])
            #stream.filter(follow_list,track_list,languages = ["en"])
        #i = i + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'

