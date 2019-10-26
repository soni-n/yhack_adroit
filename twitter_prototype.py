from twython import Twython

twitter_credentials = {
    'client_key_secret': 'q3LWUS9zrpazVcJ2pYEzXG71DJ43XYsiZxcIRVoskmIH99Bjq5',
    'client_key': 'HWD7u9Bn0pHRaBtdzkYUASHtC',
    'access_token_secret': 'pSjOxFstUmpTy8uIE2muMIhD52Qn87D3SHt3i3sHi4ZpP',
    'access_token': '1187917483300261891-Lr3IUJQTdqxUymbZnTz75Eq7rWGNyQ'
}

twitter = Twython(twitter_credentials['client_key'], twitter_credentials['client_key_secret'])

query = twit_params = {
    'q': "JetBlue -filter:retweets",
    'count': "100",
    'lang': "en",
    'tweet_mode': 'extended',
    'result_type': 'recent'
}

r = twitter.search(**query)

tweet_text = ''
tweets = []
for tweet in r['statuses']:
    tweet_text += tweet['full_text'] \
                      .replace("\n", " ") \
                      .replace("\"", "\\\"") \
                      .replace("[\uD83C\uDF00-\uDFFF\uD83D\uDC00-\uDDFF]", "") \
                      .replace("@", "") \
                  + '\n'
    tweets += [tweet_text]

with open("tweets.txt", "a") as tweets_file:
    tweets_file.write(tweet_text)