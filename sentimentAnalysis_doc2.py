import argparse
import os
import json

from google.cloud import language_v1
from google.cloud.language_v1 import enums

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Google_Service_Account_key/YHackAdroit-9cc91ec87298.json'

def sample_analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_sentiment(document, encoding_type=encoding_type)
    # Get overall sentiment of the input document

    print(u"Sentence text: {}".format(document["content"]))
    print(u"Sentence sentiment score: {}".format(response.document_sentiment.score))

    output = {}
    output["review"] = document["content"]
    output["score"] = response.document_sentiment.score

    return  output
  #   print(
  #       u"Document sentiment magnitude: {}".format(
  #           response.document_sentiment.magnitude
  #       )
  #   )
    # Get sentiment for all sentences in the document
   #  for sentence in response.sentences:
   #      print(u"Sentence text: {}".format(sentence.text.content))
   #      print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
   # #     print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
   # print(u"Language of the text: {}".format(response.language))


def analyze(filename):
    output = []
    with open(filename, 'r') as input_file:
        for i_line, line in enumerate(input_file):
            result = sample_analyze_sentiment(line)
            output.append(result)
    # json_data = json.dumps(output)
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'movie_review_filename',
        help='The filename of the movie review you\'d like to analyze.')
    args = parser.parse_args()
    jsonOutput = analyze(args.movie_review_filename)
    print(jsonOutput)

