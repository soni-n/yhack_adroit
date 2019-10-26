# Imports the Google Cloud client library
import os

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../Google_Service_Account_key/YHackAdroit-9cc91ec87298.json'

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text = u'Awesome!!!!!'
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(document=document).document_sentiment

print('Text: {}'.format(text))
print('Sentiment: {}'.format(sentiment.score))