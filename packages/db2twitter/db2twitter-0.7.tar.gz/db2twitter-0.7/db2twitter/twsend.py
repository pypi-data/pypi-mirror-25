# -*- coding: utf-8 -*-
# Copyright © 2015-2017 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# Send the tweet
'''Send the tweet'''

# 3rd party libraries imports
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import tweepy

# 3rd party libraries
from db2twitter.imagesize import ImageSize
from db2twitter.networks.mastodon import post2mastodon
from db2twitter.networks.twitter import post2twitter
from db2twitter.timetosend import TimeToSend
from db2twitter.wasposted import WasPosted

class TwSend:
    '''TwSend class'''
    def __init__(self, cfgvalues, cliargs, tweets, session, dbvalues):
        '''Constructor for the TwBuild class'''
        _, self.lastinsertid, self.firstrun = dbvalues
        self.alreadysent = False
        self.cfgvalues = cfgvalues
        self.cliargs = cliargs
        self.tweets = tweets
        # activate the sqlite db
        self.session = session
        self.main()

    def main(self):
        '''main of TwSend class'''
        for tweet in self.tweets:
            self.alreadysent = False
            # store the tweets in the sqlite3 database
            if tweet['withimage']:
                self.storetweet(tweet['data'], tweet['imagepath'])
            else:
                self.storetweet(tweet['data'], '')
            # if it is the first run, dont send all the tweets
            if not self.firstrun:
                tts = TimeToSend(self.cfgvalues)
                # are date and time ok to send the tweet?
                if tts.sendthetweet:
                    # was the tweet already sent?
                    if not self.alreadysent:
                        if tweet['withimage']:
                            # dry run mode
                            if self.cliargs.dryrun:
                                print('Should have been tweeted: {tweet} | image:{imagepath}'.format(tweet=tweet['data'], imagepath=tweet['imagepath']))
                                if 'mastodonconf' in self.cfgvalues:
                                    print('Should have been tooted: {toot} | image:{imagepath}'.format(toot=tweet['data'], imagepath=tweet['imagepath']))
                            else:
                                post2twitter(self.cfgvalues, tweet)
                                if 'mastodonconf' in self.cfgvalues:
                                    post2mastodon(self.cfgvalues, tweet)
                        else:
                            # dry run mode
                            if self.cliargs.dryrun:
                                print('Should have been tweeted: {tweet}'.format(tweet=tweet['data']))
                                if 'mastodonconf' in self.cfgvalues:
                                    print('Should have been tooted: {toot} | image:{imagepath}'.format(toot=tweet['data'], imagepath=tweet['imagepath']))
                            else:
                                post2twitter(self.cfgvalues, tweet)
                                if 'mastodonconf' in self.cfgvalues:
                                    post2mastodon(self.cfgvalues, tweet)


    def storetweet(self, tweet, tweetimage):
        '''store a tweet in sqlite database'''
        newtweet = WasPosted(tweet=tweet, tweetimage=tweetimage, lastinsertid=self.lastinsertid)
        try:
            self.session.add(newtweet)
            self.session.commit()
        except (sqlalchemy.exc.IntegrityError) as err:
            print(err)
            print('tweet already sent')
            self.session.rollback()
            self.alreadysent = True
