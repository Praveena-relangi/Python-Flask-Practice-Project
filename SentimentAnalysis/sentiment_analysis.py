import requests
import json

def sentiment_analyzer(text_to_analyse):
    """
    Analyzes the sentiment of the given text using an external API.

    Parameters:
        text_to_analyse (str): The text to analyze.

    Returns:
        dict: A dictionary containing 'label' and 'score' if successful, or an 'error' message.
    """
    # Define the URL for the sentiment analysis API
    url = 'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict'

    # Create the payload with the text to be analyzed
    payload = {"raw_document": {"text": text_to_analyse}}

    # Set the headers with the required model ID for the API
    headers = {"grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"}

    try:
        # Make a POST request to the API
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            document_sentiment = data.get('documentSentiment', {})
            label = document_sentiment.get('label')
            score = document_sentiment.get('score')

            if label is not None and score is not None:
                return {'label': label, 'score': score}
            else:
                return {'error': "Incomplete sentiment data in response"}

        # Handle API error responses
        return {'error': f"API request failed with status code {response.status_code}"}

    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        return {'error': f"Network error: {e}"}

    except json.JSONDecodeError:
        # Handle invalid JSON responses
        return {'error': "Invalid JSON response from server"}
