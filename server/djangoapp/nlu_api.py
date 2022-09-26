import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions


authenticator = IAMAuthenticator(apikey)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
)

natural_language_understanding.set_service_url(url)
def get_sentiment(dealerreview):
    response = natural_language_understanding.analyze(
        text=dealerreview,
        language='en',
        features=Features(sentiment=SentimentOptions())).get_result()

    return response['sentiment']['document']['label']
