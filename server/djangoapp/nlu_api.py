import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions

url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/da1b342d-af00-4031-919d-a0119f3f077f/v1/analyze?version=2022-04-07"
apikey="M4Yme5VOu4ej-2MnkE7GKqYOQgc7W2mcIvEgmSphl22r"

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
