
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
import os
from twython import Twython

from google.cloud import language
from google.cloud.language import enums

app = Flask(__name__)

twitter_credentials = {
    'client_key_secret': 'q3LWUS9zrpazVcJ2pYEzXG71DJ43XYsiZxcIRVoskmIH99Bjq5',
    'client_key': 'HWD7u9Bn0pHRaBtdzkYUASHtC',
    'access_token_secret': 'pSjOxFstUmpTy8uIE2muMIhD52Qn87D3SHt3i3sHi4ZpP',
    'access_token': '1187917483300261891-Lr3IUJQTdqxUymbZnTz75Eq7rWGNyQ'
}

@app.route('/')
def hello_world():
    twitter = Twython(twitter_credentials['client_key'], twitter_credentials['client_key_secret'])
    query = {
        'q': "%s -filter:retweets" % request.args.get('query'),
        'count': request.args.get('count'),
        'lang': "en",
        'tweet_mode': 'extended',
        'result_type': 'recent'
    }
    r = twitter.search(**query)

    tweets = []
    for tweet in r['statuses']:
        tweet_text = tweet['full_text'] \
                      .replace("\n", " ") \
                      .replace("\"", "\\\"") \
                  + '\n'
        tweets += [tweet_text]

    return str(analyze(tweets))

def sample_analyze_sentiment(text_content):

    client = language.LanguageServiceClient()

    document = {"content": text_content, "type": enums.Document.Type.PLAIN_TEXT, "language": "en"}

    response = client.analyze_sentiment(document, encoding_type=enums.EncodingType.UTF8)
    # Get overall sentiment of the input document

    output = {}
    output["review"] = document["content"]
    output["score"] = response.document_sentiment.score

    return output


def analyze(content):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/digit42/adroit/google_credentials.json'
    output = []
    for i_line, line in enumerate(content):
        result = sample_analyze_sentiment(line)
        output.append(result)
    return output