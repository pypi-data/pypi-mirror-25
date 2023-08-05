# db2twitter

db2twitter automatically extracts fields from your database, use them to feed a template of
tweet and send the tweet.

If you would like, you can [support the development of this project on Liberapay](https://liberapay.com/carlchenet/).
Alternatively you can donate cryptocurrencies:

- BTC: 1BcdXCcLKN9PRpp6qw23FYkYuVp59dKZix
- XMR: 4Cxwvw9V6yUehv832FWPTF7FSVuWjuBarFd17QP163uxMaFyoqwmDf1aiRtS5jWgCiRsi73yqedNJJ6V1La2joznUDzkmvBr6KKHT7Dvzj

### Quick Install

* Install db2twitter from PyPI

        # pip3 install db2twitter

* Install db2twitter from sources

        # tar zxvf db2twitter-0.7.tar.gz
        # cd db2twitter
        # python3.4 setup.py install
        # # or
        # python3.4 setup.py install --install-scripts=/usr/bin

### Use db2twitter

* Create or modify db2twitter.ini file in order to configure db2twitter:

        [mastodon]
        instance_url=https://framapiaf.org
        user_credentials=/etc/db2twitter/credentials/db2twitter_usercred.txt
        client_credentials=/etc/db2twitter/credentials/db2twitter_clientcred.txt
        visibility=public

        [twitter]
        consumer_key=pPskvBmlE1yatbrFsLMdQL1r3m
        consumer_secret=lkjerpleRZER4xf948sfsrfgmlkezrZERgl1234ljfeqIdIie4
        access_token=1234823497-912qsdfkerR913U5hjzer34234kerPzAQHoP9ez
        access_token_secret=ljsERZE987h8k1klr123k9kezr09h134HLKJER98er5K1
        tweet={} recrute un {} https://www.linuxjobs.fr/jobs/{}
        hashtags=devops,linux,debian,redhat,python,java,php,mysql,postgresql
        upper_first_char=true

        [database]
        ; use the following for MySQL - you need mysql_connector_python
        dbconnector=mysql+mysqlconnector
        ; use the following for PostgreSQL - you need psycopg2 python library
        ; dbconnector=postgresql+psycopg2
        dbhost=localhost
        database=jobboard
        dbuser=jobboard
        dbpass=V3rYS3cr3t
        dbtables=jobs,
        jobs_rows=companyname,jobtitle,id,logo
        jobs_image=true
        ; send custom sql filter to the request with the following line
        ; jobs_sqlfilter=status=1

        [sqlite]
        sqlitepath=/home/chaica/progra/python/db2twitter/db2twitter.db

        [media]
        image_path=/var/www/jobboard/images/

        [timer]
        days=mon-fri,
        hours=0-11,14-17,

        [circle]
        last_tweets=3
        each_time=2
        ; no_image=true


* Launch db2twitter

        $ db2twitter /path/to/db2twitter.ini

### Authors

Carl Chenet <chaica@ohmytux.com>

### License

This software comes under the terms of the GPLv3+. See the LICENSE file for the complete text of the license.
