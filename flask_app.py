
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
import os
import collections
import json
from twython import Twython
import math

from google.cloud import language_v1
from google.cloud.language_v1 import enums

app = Flask(__name__)

twitter_credentials = {
    'client_key_secret': 'q3LWUS9zrpazVcJ2pYEzXG71DJ43XYsiZxcIRVoskmIH99Bjq5',
    'client_key': 'HWD7u9Bn0pHRaBtdzkYUASHtC',
    'access_token_secret': 'pSjOxFstUmpTy8uIE2muMIhD52Qn87D3SHt3i3sHi4ZpP',
    'access_token': '1187917483300261891-Lr3IUJQTdqxUymbZnTz75Eq7rWGNyQ'
}

@app.route('/')
def production():

    mpp = 100

    twitter = Twython(twitter_credentials['client_key'], twitter_credentials['client_key_secret'])
    count = int(request.args.get('count'))

    query = {
        'q': "%s -filter:retweets" % request.args.get('query'),
        'count': str(count%mpp),
        'lang': "en",
        'tweet_mode': 'extended',
        'result_type': 'recent'
    }


    twitter_response = twitter.search(**query)
    statuses = twitter_response['statuses']

    min_id = twitter_response['search_metadata']['max_id']
    for tweet in twitter_response['statuses']:
        if tweet['id'] < min_id:
            min_id = tweet['id']


    query['count'] = mpp

    for i in range(0, math.floor((count-1)/mpp)):
        query['max_id'] = min_id-1
        twitter_response = twitter.search(**query)
        statuses += twitter_response['statuses']

        min_id = twitter_response['search_metadata']['max_id']
        for tweet in twitter_response['statuses']:
            if tweet['id'] < min_id:
                min_id = tweet['id']


    tweets = []
    for tweet in statuses:
        tweet_text = tweet['full_text'] \
                      .replace("\n", " ") \
                      .replace("\"", "\\\"") \
                  + '\n'
        tweets += [tweet_text]

    result = analyze(tweets)
    output = {}
    output['sentiments'] = result[0]
    output['concerns'] = result[1]

    return str(json.dumps(output))


def sample_analyze_entities(text_content):
    entityAnalysis = []
    client = language_v1.LanguageServiceClient()
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8
    response = client.analyze_entities(document, encoding_type=encoding_type)
    for entity in response.entities:
        if enums.Entity.Type(entity.type) == (enums.Entity.Type.OTHER or enums.Entity.Type.EVENT):
            entityAnalysis.append("{}".format(entity.name))

    return entityAnalysis

def sample_analyze_sentiment(text_content):
    output = {}
    entityAnalysis = []
    client = language_v1.LanguageServiceClient()
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8
    response = client.analyze_sentiment(document, encoding_type=encoding_type)
    # print(u"Sentence text: {}".format(document["content"]))
    # print(u"Sentence sentiment score: {}".format(response.document_sentiment.score))
    if (response.document_sentiment.score < 0.1):
        output["review"] = document["content"]
        output["score"] = response.document_sentiment.score
        entityAnalysis = sample_analyze_entities(document["content"])
    return  output, entityAnalysis

def extractTopTenConcernAreas(entityAnalysis):
    #concernAreas = []
    # for i in range(len(entityAnalysis)):
    #     concernAreas.append(entityAnalysis[i].name)
    concernAreas = [item for sublist in entityAnalysis for item in sublist]
    concerns = list(map(lambda x: x[0], collections.Counter(concernAreas).most_common()))
    return concerns[:20]

def analyze(lines):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/digit42/adroit/google_credentials.json'
    negativeSentiments = []
    entityData = []
    for i_line, line in enumerate(lines):
        result = sample_analyze_sentiment(line)
        if result[0] != {}: negativeSentiments.append(result[0])
        entityData.append(result[1])

    topConcernAreas = extractTopTenConcernAreas(entityData)
    return negativeSentiments, topConcernAreas


