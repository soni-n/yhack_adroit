from twython import Twython
from google.cloud import language
from google.cloud import automl_v1beta1 as automl
import nltk
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
import sys


twitter_credentials = {
    'client_key_secret': 'q3LWUS9zrpazVcJ2pYEzXG71DJ43XYsiZxcIRVoskmIH99Bjq5',
    'client_key': 'HWD7u9Bn0pHRaBtdzkYUASHtC',
    'access_token_secret': 'pSjOxFstUmpTy8uIE2muMIhD52Qn87D3SHt3i3sHi4ZpP',
    'access_token': '1187917483300261891-Lr3IUJQTdqxUymbZnTz75Eq7rWGNyQ'
}


twitter = Twython(twitter_credentials['client_key'], twitter_credentials['client_key_secret'])
google_automl = automl.AutoMlClient()
google_predictions = automl.PredictionServiceClient()

model_full_id = google_automl.model_path(
    'yhackadroit', 'us-east4', 'model_id'
)


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
    tweet_text += tweet['full_text'].replace("\n", " ").replace("\"", "\\\"") + '\n'
    tweets += [tweet_text]

with open("tweets.txt", "a") as tweets_file:
    tweets_file.write(tweet_text)



payload = {'text_snippet': {'content': tweet_text, 'mime_type': 'text/plain'}}
response = google_predictions.predict(model_full_id, payload, {})


for result in response.payload:
    print("Predicted sentiment label: {}".format(result.text_sentiment.sentiment))

for key, data in response.metadata.items():
    if key == 'sentiment_score':
        print("Normalized sentiment score: {}".format(data))


# training_data = [
#     (['test', 'which', 'is', 'tokenized'], 'positive')
# ]
#
# analyzer = SentimentAnalyzer()
#
# for tweet in tweets:
#     unigram_feats = analyzer.unigram_word_feats(
#         analyzer.all_words([mark_negation(doc) for doc in training_data]), min_freq=3)
#     analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
#


