# -*- coding: utf-8 -*-
"""
Transform Activity Streams objects into CSV rows for use with metrify.awk

Kevin Driscoll, kedrisco@usc.edu, public domain, 2013


INPUT 

Input files consist of tweets in Activity Streams JSON format, 
one per line, as they are returned from Gnip PowerTrack.

Gnip Activity Streams
http://support.gnip.com/customer/portal/articles/477765-twitter-activity-streams-format


OUTPUT

Output conforms to the CSV output of the modified yourTwapperKeeper:
http://mappingonlinepublics.net/2011/06/21/switching-from-twapperkeeper-to-yourtwapperkeeper/

Tweets are sorted in ascending order according to the value in the "time" column.

text                tweet text
to_user_id			user_id if the tweet begins with @username
from_user			screen_name of the user sending the tweet
id	        		numeric id of the tweet (must be stored as a string)
from_user_id	    user_id of the user sending the tweet
iso_language_code	two letter language code, e.g. "en"
source			    application sending this tweet (may include HTML)
profile_image_url	URL pointing to the sending user's profile photo
geo_type			type of location information included, e.g. "Point"
geo_coordinates_0	latitude
geo_coordinates_1   longitude	
created_at			idiosyncraticly formed human-readable date and time
time                Seconds since UNIX epoch, PHP time() function, 
                        http://php.net/manual/en/function.time.php
                        https://github.com/540co/yourTwapperKeeper/blob/master/function.php#L100


USAGE

The output cannot be piped directly into metrify.awk.
Instead store the output in an intermediate file, e.g.:

$ python activitystreams2ytk.py tweets.json > tweets.csv
$ gawk -F , -f metrify.awk time="hour" divisions=90,99,1 tweets.csv > metrics.csv

Read more about using metrify.awk here:
http://mappingonlinepublics.net/2012/01/31/more-twitter-metrics-metrify-revisited/


"""

import calendar
import dateutil.parser
import fileinput
import json

YTK_DATETIME_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'
SEPARATOR = ','

headings = [
    "text",
	"to_user_id",
	"from_user",
	"id",
	"from_user_id",
	"iso_language_code",
	"source",
	"profile_image_url",
	"geo_type",
	"geo_coordinates_0",
	"geo_coordinates_1",
	"created_at",
	"time"
]

# Read Activity Streams objects from input file
tweets = []
for line in fileinput.input():
    tweet = json.loads(line.strip())
    # Create a datetime object from the postedTime string 
    tweet['postedTimeObj'] = dateutil.parser.parse(tweet.get('postedTime'))
    # Calculate seconds since the UNIX epoch
    tweet['time'] = calendar.timegm(tweet['postedTimeObj'].timetuple())
    tweets.append(tweet)

# Output a row of headings
row = unicode(SEPARATOR.join(headings))
print row.encode('utf-8')

# Iterate over tweets in ascending chronological order
for tweet in sorted(tweets, key=lambda t: t['time']):

    # If this is a @-reply, extract the targeted username and user_id 
    if 'inReplyTo' in tweet:
        # Sort mentions by order they appear in the tweet text
        mentions = sorted(tweet['twitter_entities']['user_mentions'], 
                            key=lambda m: m['indices'][0])[0]['id_str']
        to_username = mentions[0]['screen_name']
        to_user_id = mentions[0]['id_str']
    else:
        to_username = '' 
        to_user_id = ''

    # If this is geocoded, extract the location information
    if 'geo' in tweet:
        geo = tweet['geo']['type']
        coords  = tweet.get('geo', {}).get('coordinates', [0, 0])
    else:
        geo = ''
        coords = (0, 0)

    # Sequence and format according to the column order
    cols = [
        tweet['body'].replace('\n','').replace('\r','').replace(SEPARATOR,''),
        to_user_id,
        tweet['actor']['preferredUsername'],
        tweet['id_str'],
        tweet['actor']['id_str'],
        '&'.join(tweet['actor']['languages']), # e.g., en&es
        tweet['generator']['displayName'],
        tweet['actor']['image'],
        geo,
        coords[0],
        coords[1],
        tweet['postedTimeObj'].strftime(YTK_DATETIME_FORMAT),
        tweet['time']
    ]

    # Combine into one Unicode string and print
    row = u''
    for col in cols:
        row += u'{0}{1}'.format(unicode(col, SEPARATOR))
    row = row[:-1] 
    print row.encode('utf-8')

