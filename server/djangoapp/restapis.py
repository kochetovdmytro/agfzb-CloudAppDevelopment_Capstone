import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from .nlu_api import get_sentiment
from requests.auth import HTTPBasicAuth
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key));
def get_request(url, **kwargs):
    print("GET from {} ".format(url))
    try:
        
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                     params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except:
        # If any error occurs
        print("Network exception occurred")
    
    return json_data


def post_request(url, json_payload, **kwargs):
    print("POST to {} ".format(url))
    try:
        print(url)
        print(json_payload)
        response = requests.post(url, json=json_payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except Exception as e: 
        # If any error occurs
        print("Network exception occurred")
        print(str(e))
        return
    return json_data    
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print('first')
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], state=dealer_doc["state"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc["short_name"])
            results.append(dealer_obj)

    return results
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_state(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], state=dealer_doc["state"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc["short_name"])
            results.append(dealer_obj)

    return results



def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            dealer_doc["sentiment"] = get_sentiment(dealer_doc["review"])
            # Create a CarDealer object with values in `doc` object
            dealer_obj = DealerReview(car_make=dealer_doc["car_make"], car_model=dealer_doc["car_model"], car_year=dealer_doc["car_year"],
                                   dealership=dealer_doc["dealership"], id=dealer_doc["id"], name=dealer_doc["name"],
                                   purchase=dealer_doc["purchase"], purchase_date=dealer_doc["purchase_date"], review=dealer_doc["review"], sentiment=dealer_doc["sentiment"])
            results.append(dealer_obj)

    return results
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text

    






# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



