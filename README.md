# Transform Activity Streams objects into CSV rows for use with metrify.awk

Kevin Driscoll, kedrisco@usc.edu, public domain, 2013


## Input

Input files consist of tweets in Activity Streams JSON format, 
one per line, as they are returned from Gnip PowerTrack.

Gnip Activity Streams
http://support.gnip.com/customer/portal/articles/477765-twitter-activity-streams-format


## Output

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


## Usage

The output cannot be piped directly into metrify.awk.
Instead store the output in an intermediate file, e.g.:

$ python activitystreams2ytk.py tweets.json > tweets.csv
$ gawk -F , -f metrify.awk time="hour" divisions=90,99,1 tweets.csv > metrics.csv

Read more about using metrify.awk here:
http://mappingonlinepublics.net/2012/01/31/more-twitter-metrics-metrify-revisited/

