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

'''WasPosted mapping for SQLAlchemy'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

MYBASE = declarative_base()

class WasPosted(MYBASE):
    '''WasPosted mapping for SQLAlchemy'''
    __tablename__ = 'wasposted'
    twid = Column(Integer, primary_key=True)
    tweet = Column(String, unique=True)
    tweetimage = Column(String, unique=False)
    lastinsertid = Column(Integer)
    lastcircled = Column(Boolean, default=False)
