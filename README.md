# Transform Activity Streams objects into CSV rows for use with metrify.awk

Kevin Driscoll, kedrisco@usc.edu, public domain, 2013


## Input

Input files consist of tweets in Activity Streams JSON format, 
one per line, as they are returned from [Gnip PowerTrack](http://support.gnip.com/customer/portal/articles/477765-twitter-activity-streams-format).


## Output

Output conforms to the CSV output of the [modified yourTwapperKeeper](http://mappingonlinepublics.net/2011/06/21/switching-from-twapperkeeper-to-yourtwapperkeeper/):

Tweets are sorted in ascending order according to the value in the "time" column.

*_text_: tweet text 
*_to_user_id_: user_id if the tweet begins with @username
*_from_user_: screen_name of the user sending the tweet 
*_id_: numeric id of the tweet (must be stored as a string) 
*_from_user_id_: user_id of the user sending the tweet
*_iso_language_code_: two letter language code, e.g. "en"
*_source_: application sending this tweet (may include HTML)
*_profile_image_url_: URL pointing to the sending user's profile photo
*_geo_type_: type of location information included, e.g. "Point"
*_geo_coordinates_0_: latitude
*_geo_coordinates_1_: longitude   
*_created_at_: idiosyncraticly formed human-readable date and time 
* _time_: created_at in Seconds since UNIX epoch via [PHP time() function](http://php.net/manual/en/function.time.php) 

## Usage

The output cannot be piped directly into metrify.awk.
Instead store the output in an intermediate file, e.g.:

```shell
$ python activitystreams2ytk.py tweets.json > tweets.csv
$ gawk -F , -f metrify.awk time="hour" divisions=90,99,1 tweets.csv > metrics.csv
```

Read more about using metrify.awk at the [Mapping Online Publics](http://mappingonlinepublics.net/2012/01/31/more-twitter-metrics-metrify-revisited/) blog.

