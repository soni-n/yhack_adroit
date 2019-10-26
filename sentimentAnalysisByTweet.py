"""Demonstrates how to make a simple call to the Natural Language API."""

import argparse
import os

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud.language_v1.gapic.enums import EncodingType

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/miles/PycharmProjects/kvetchtech/api/google_credentials.json'


def analyze(filename):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    with open(filename, 'r') as input_file:
        for i_line, line in enumerate(input_file):
            document = types.Document(
                content=line,
                type=enums.Document.Type.PLAIN_TEXT
            )
            result = client.analyze_sentiment(document)
            print("Tweet #%d: %.3f" % (i_line, result.document_sentiment.score))


if __name__ == '__main__':
    analyze('tweets.txt')