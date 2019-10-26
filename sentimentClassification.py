# Imports the Google Cloud client library
import os
import twython

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Set Google credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../Google_Service_Account_key/YHackAdroit-9cc91ec87298.json'

twitter_credentials = {
    'client_key_secret': 'q3LWUS9zrpazVcJ2pYEzXG71DJ43XYsiZxcIRVoskmIH99Bjq5',
    'client_key': 'HWD7u9Bn0pHRaBtdzkYUASHtC',
    'access_token_secret': 'pSjOxFstUmpTy8uIE2muMIhD52Qn87D3SHt3i3sHi4ZpP',
    'access_token': '1187917483300261891-Lr3IUJQTdqxUymbZnTz75Eq7rWGNyQ'
}

twitter = Twython(twitter_credentials['client_key'], twitter_credentials['client_key_secret'])



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