import argparse
import os
import collections
from builtins import map, len, range

from google.cloud import language_v1
from google.cloud.language_v1 import enums

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/miles/PycharmProjects/kvetchtech/api/google_credentials.json'
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
            #analysis = {}
            # analysis['Entity_type'] = "{}".format(enums.Entity.Type(entity.type).name)
            #analysis['entity_names'] = "{}".format(entity.name)
            #analysis['salience_score'] = "{}".format(entity.salience)
            entityAnalysis.append("{}".format(entity.name))
        #entityAnalysis.append(analysis)
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

def analyze(filename):
    negativeSentiments = []
    entityData = []
    with open(filename, 'r') as input_file:
        for i_line, line in enumerate(input_file):
            result = sample_analyze_sentiment(line)
            if result[0] != {}: negativeSentiments.append(result[0])
            entityData.append(result[1])
    topConcernAreas = extractTopTenConcernAreas(entityData)
    return negativeSentiments, topConcernAreas

if __name__ == '__main__':
    result = analyze('/home/miles/PycharmProjects/yhack_adroit/tweets.txt')
    output = {}
    output['sentiments'] = result[0]
    output['concerns'] = result[1]
    print("Top 20 concerns")
    print(output['concerns'])

