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
# along with this program.  If not, see <http://www.gnu.org/licenses/

# Main class
'''Main class'''

# standard libraries imports
import configparser
import os.path
import sys

# 3rd party libraries imports
from sqlalchemy import desc

# app libraries imports
from db2twitter.wasposted import WasPosted

def refresh(cfgvalues, tweets, sqlitesession, dbvalues)
    '''refresh the content of the database'''
    newtweet = WasPosted(tweet=tweet, tweetimage=tweetimage, lastinsertid=self.lastinsertid)
    try:
        self.session.add(newtweet)
        self.session.commit()
    except (sqlalchemy.exc.IntegrityError) as err:
        print(err)
        print('tweet already sent')
        self.session.rollback()
        self.alreadysent = True
